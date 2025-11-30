import os
import time
from cudatext import *
from cudatext_keys import *
from cudax_lib import get_translation

_ = get_translation(__file__) # I18N

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')

COMMAND_PALETTE_COMMAND_CODE = 2582

delay_ms = 300
shift_command_id = COMMAND_PALETTE_COMMAND_CODE
shift_command_text = ""
ctrl_command_id = COMMAND_PALETTE_COMMAND_CODE
ctrl_command_text = "opened file:"

prior_hotkey_time = None
prior_hotkey = None

class Command:

    def __init__(self):
        global delay_ms
        global shift_command_id
        global shift_command_text
        global ctrl_command_id
        global ctrl_command_text

        global prior_hotkey_time
        
        delay_ms = int(ini_read(fn_config, 'double_shift', 'delay_ms', str(delay_ms)))

        shift_command_id = int(ini_read(fn_config, 'double_shift', 'shift_command_id', str(shift_command_id)))
        shift_command_text = ini_read(fn_config, 'double_shift', 'shift_command_text', shift_command_text)

        ctrl_command_id = int(ini_read(fn_config, 'double_shift', 'ctrl_command_id', str(ctrl_command_id)))
        ctrl_command_text = ini_read(fn_config, 'double_shift', 'ctrl_command_text', ctrl_command_text)

        
        ten_minutes = 600 
        prior_hotkey_time = time.time() - ten_minutes

    def config(self):
        ini_write(fn_config, 'double_shift', 'delay_ms', str(delay_ms))

        ini_write(fn_config, 'double_shift', 'shift_command_id', str(shift_command_id))
        ini_write(fn_config, 'double_shift', 'shift_command_text', shift_command_text)

        ini_write(fn_config, 'double_shift', 'ctrl_command_id', str(ctrl_command_id))
        ini_write(fn_config, 'double_shift', 'ctrl_command_text', ctrl_command_text)

        file_open(fn_config)

    def on_key_up(self, ed_self, key, state):
        global prior_hotkey_time
        global call_counter
        global delay_ms
        global prior_hotkey

        if key != VK_CONTROL and key != VK_SHIFT:
            return

        if key != prior_hotkey:
            prior_hotkey = key
            prior_hotkey_time = time.time()
            return

        ms_since_prior_hotkey = (time.time() - prior_hotkey_time) * 1000
        prior_hotkey_time = time.time()

        if ms_since_prior_hotkey < delay_ms:
            if key == VK_SHIFT:
                ed.cmd(shift_command_id, shift_command_text)  
            elif key == VK_CONTROL:
                ed.cmd(ctrl_command_id, ctrl_command_text)  
                