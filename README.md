# pyUIauto

[![PyPi version](https://badgen.net/pypi/v/pyuiauto/)](https://pypi.org/project/pyuiauto/)
[![PyPi license](https://badgen.net/pypi/license/pyuiauto/)](https://pypi.org/project/pyuiauto/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyuiauto.svg)](https://pypi.python.org/pypi/pyuiauto/)


<!--| Tests       | Status                                                                                                                  |
| :---------- | :---------------------------------------------------------------------------------------------------------------------: |
| Development | ![Development Tests](https://github.com/harveyf2801/pyUIauto/actions/workflows/run_dev_tests.yml/badge.svg?branch=main)       |
| Build       | ![Build Tests](https://github.com/harveyf2801/pyUIauto/actions/workflows/build_wheel.yml/badge.svg?branch=main) |-->

Python UI Automation library, for cross-platform applications, interfacing through the accessibility API.

## Description

This library / framework takes two popular UI automation libraries and combines their functionality by wrapping them into custom components and creating methods that function in similar ways for both OS. This project was originally designed as part of a QA automation project to perform end-to-end testing on desktop applications.

> ⤴️: **Open source**: This project is open source and welcomes any pull requests and further improvements!

## Getting Started

### Dependencies

Python Packages:

- pywinauto (Windows / Linux)
- atomacos (MacOS)
- pyautogui

OS Compatibility:

- Windows
- MacOS

( Currently untested on Linux )

## Example

```python
# Import the tools needed
from platform import system
import os
from pyuiauto.application import UIApplication
from pyuiauto.components import UIButton

# Finding the path location of the application
app_paths = {
  "Darwin": "/Applications/Visual Studio Code.app",
  "Windows": os.path.expanduser('~') + "\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
}

if system() in app_paths:
  appPath = app_paths[system()]
else:
  raise NotImplementedError("The current OS is not currently supported: " + system())

# Setting up an application template, launching the app, and connecting to it
app = UIApplication(appName = "Visual Studio Code", appPath = appPath)
app.launchApp()
app.connectApp()

# Finding the window component and searching for elements within this window component
main_window = app.window(title = "Visual Studio Code", timeout = 2)
main_window.findR(title = "Toggle Primary Side Bar (Ctrl+B)", control_type = UIButton).press() '''  press will invoke a button without manually moving the mouse and clicking it 
                                                                                          (a button could be invoked even if it isn't currently visible)  '''
main_window.findR(title = "Open Folder", control_type = UIButton).click() ''' however, click will move the mouse to the button location and click it
                                                                    (sometimes this can be more reliable) '''

# Closing the window and terminating the application
main_window.close()
app.terminateApp()
```

## Authors

ex. Harvey Fretwell

ex. [pyWinAuto](https://github.com/pywinauto/pywinauto/tree/master)

ex. [atomacos](https://github.com/daveenguyen/atomacos)

ex. [pyAutoGUI](https://github.com/asweigart/pyautogui)

## Version History

- 0.1
  - Initial Release
  - 0.1.1
    - Added UISystemTrayIcon and UIPopupMenu manager
  - 0.1.4
    - Fixed some issues with setValue() method on buttons and menus
  - 0.1.5
    - Added context managers for better popup menu handling
  - 0.1.6
    - Added isOnTop method for components
    - Fixed isVisible method for components
    - Added checks for components existing in helper methods
  - 0.1.7
    - Added MacOS compatibility
    - Fixed getValue method for mac on menu items (with a bit of a work around ... hoping to find a better solution soon)
    - Fixed menu path select and system tray popup select methods on mac
  - 0.1.8
    - Fixed progress bar get value method
    - Added better python intellisense for pylance
    - Added further checks for system tray icon
    - Updated application.py
    - Upgraded package versions
  - 0.1.9
    - Added CheckBox component
  - 0.1.10
    - Added popup button for MacOS
  - 0.1.11
    - Fixed `getChildren`
    - Fixed popup menu navigation
  - 0.1.12
    - Fixed Windows UIRadioButton `getValue`

## Acknowledgments

- [pyWinAuto](https://github.com/pywinauto/pywinauto/tree/master)
- [atomacos](https://github.com/daveenguyen/atomacos)
- [pyAutoGUI](https://github.com/asweigart/pyautogui)
