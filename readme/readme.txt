Plugin for CudaText.

Double-Shift hotkeys for CudaText text editor. Behavior similar to JetBrains "Search Everywhere" function. 

Config file is supported: (CudaText)/settings/plugins.ini:

[double_shift]
delay_ms=300
shift_command_id=2582
shift_command_text=
ctrl_command_id=2582
ctrl_command_text=opened file:

Options in ini-file are:

- delay_ms: Time interval between two key releases
- shift_command_id: command id to call for Double-Shift
- shift_command_text: command id additional parameters (if required)
- ctrl_command_id: command id to call for Double-Control
- ctrl_command_text: command id additional parameters (if required)

Author: Dmitry Fedorov (https://github.com/dimon40001)
Lincese: MIT
