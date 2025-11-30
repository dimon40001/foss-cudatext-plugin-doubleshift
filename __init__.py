import os
import time
from cudatext import *
from cudatext_keys import *
import cudatext_cmd as cmds

CONFIG_SECTION = 'double_shift'
DELAY_MS_KEY = "delay_ms"
SHIFT_CMD_ID_KEY = 'shift_command_id'
SHIFT_CMD_TEXT_KEY = 'shift_command_text'
CTRL_CMD_ID_KEY = 'ctrl_command_id'
CTRL_CMD_TEXT_KEY = 'ctrl_command_text'
TEN_MINUTES = 600

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')

delay_ms = 200
shift_command_id = cmds.cmd_DialogCommands
shift_command_text = ""
ctrl_command_id = cmds.cmd_DialogCommands
ctrl_command_text = "opened file:"

prior_hotkey_pressed_time = None
prior_hotkey_pressed = None
first_release_happened = False
first_press_happened = False


class Command:

    def reset_state(self):
        global prior_hotkey_pressed
        global prior_hotkey_pressed_time
        global first_release_happened
        global first_press_happened

        prior_hotkey_pressed_time = time.time() - TEN_MINUTES
        prior_hotkey_pressed = None
        first_release_happened = False
        first_press_happened = False

    def __init__(self):
        global delay_ms
        global shift_command_id
        global shift_command_text
        global ctrl_command_id
        global ctrl_command_text

        delay_ms = int(ini_read(fn_config, CONFIG_SECTION, DELAY_MS_KEY, str(delay_ms)))

        shift_command_id = int(ini_read(fn_config, CONFIG_SECTION, SHIFT_CMD_ID_KEY, str(shift_command_id)))
        shift_command_text = ini_read(fn_config, CONFIG_SECTION, SHIFT_CMD_TEXT_KEY, shift_command_text)

        ctrl_command_id = int(ini_read(fn_config, CONFIG_SECTION, CTRL_CMD_ID_KEY, str(ctrl_command_id)))
        ctrl_command_text = ini_read(fn_config, CONFIG_SECTION, CTRL_CMD_TEXT_KEY, ctrl_command_text)

        self.reset_state()

    def config(self):
        ini_write(fn_config, CONFIG_SECTION, DELAY_MS_KEY, str(delay_ms))

        ini_write(fn_config, CONFIG_SECTION, SHIFT_CMD_ID_KEY, str(shift_command_id))
        ini_write(fn_config, CONFIG_SECTION, SHIFT_CMD_TEXT_KEY, shift_command_text)

        ini_write(fn_config, CONFIG_SECTION, CTRL_CMD_ID_KEY, str(ctrl_command_id))
        ini_write(fn_config, CONFIG_SECTION, CTRL_CMD_TEXT_KEY, ctrl_command_text)

        file_open(fn_config)

        lines = [ed.get_text_line(i) for i in range(ed.get_line_count())]
        try:
            index = lines.index('[' + CONFIG_SECTION + ']')
            ed.set_caret(0, index)
        except:
            pass

    def on_key(self, ed_self, key, state):
        global prior_hotkey_pressed_time
        global prior_hotkey_pressed
        global first_release_happened
        global first_press_happened

        if key != VK_CONTROL and key != VK_SHIFT:
            return
        if key != prior_hotkey_pressed:
            self.reset_state()

        # CudaText emits on_key() events for pressed-and-hold key
        # in such a way, that there are "presses" without the releases
        # this check handles that
        if not first_press_happened:
            first_press_happened = True
            prior_hotkey_pressed = key
            prior_hotkey_pressed_time = time.time()

    def on_key_up(self, ed_self, key, state):
        global prior_hotkey_pressed_time
        global prior_hotkey_pressed
        global first_release_happened

        if key != VK_CONTROL and key != VK_SHIFT:
            return

        if first_release_happened:
            ms_since_prior_hotkey_press = (time.time() - prior_hotkey_pressed_time) * 1000

            self.reset_state()
            if ms_since_prior_hotkey_press < delay_ms:
                if key == VK_SHIFT:
                    ed.cmd(shift_command_id, shift_command_text)
                elif key == VK_CONTROL:
                    ed.cmd(ctrl_command_id, ctrl_command_text)
        else:
            first_release_happened = True
