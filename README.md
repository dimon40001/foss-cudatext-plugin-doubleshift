# Double-Shift plugin for Cuda Text

Double-Shift hotkeys for CudaText text editor. Behavior similar to JetBrains "Search Everywhere" function. 

Implementation based on `on_key()` event functionality.

## Installation option:

1. From Cudatext menu

- Go to `Plugins > Addons Manager > Install from Git...`
- provide Git repository URL: `https://github.com/dimon40001/foss-cudatext-plugin-doubleshift` 

2.  Manual

- clone repository to the Cudatext `py/` folder
- restart CudaText

## Settings

To manage own settings plugin creates `double_shift` section in the `plugins.ini`

Configuration:
```
[double_shift]

# Time interval (in milliseconds) between each key release to detect it as the "double" action
delay_ms=300 

# call Command Palette (usually bind to F1 key) and show all commands
shift_command_id=2582 
shift_command_text= # ...with empty parameters

# call Command Palette to search in opened files
ctrl_command_id=2582 # call Command Palette
ctrl_command_text=opened file: # ...
```
