# pyUIauto

Python UI Automation library, for cross-platform applications, interfacing through the accessibility API.

## Description

This library / framework takes two popular UI automation libraries and combines their functionality by wrapping them into custom components and creating methods that function in similar ways for both OS. This project was originally designed as part of a QA automation project to perform end-to-end testing on desktop applications.

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

Python Packages:
- pywinauto (Windows / Linux)
- atomacos (MacOS)
- pyautogui

OS Compatibility:
- Windows
- MacOS

( Currently untested on Linux )

## Example

Opening a folder in Visual Studio Code using the python automation library:

```python
# Import the tools needed
from platform import system
import os
from pyuiauto.application import UIApplication
from pyuiauto.components import UIButton

# Finding the path location of the application
app_paths = {
  "Darwin": "/Applications/Visual Studio Code.app",
  "Windows": os.path.expanduser('~') + "\AppData\Local\Programs\Microsoft VS Code\Code.exe"
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
ex. (https://github.com/pywinauto/pywinauto/tree/master)
ex. (https://github.com/daveenguyen/atomacos)
ex. (https://github.com/asweigart/pyautogui)

## Version History

* 0.1
    * Initial Release

## Acknowledgments

* [pyWinAuto](https://github.com/pywinauto/pywinauto/tree/master)
* [atomacos](https://github.com/daveenguyen/atomacos)
* [pyAutoGUI](https://github.com/asweigart/pyautogui)