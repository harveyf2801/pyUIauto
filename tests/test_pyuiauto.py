from platform import system
import os
import pytest
import logging

from pyuiauto.src.application import UIApplication
from pyuiauto.src.components import UIWindow, UIButton, UISlider
from pyuiauto import __version__

# pip installed modules
try:
        from pyautogui import hotkey
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pyautogui')

app_paths = {
  "Darwin": "/Applications/EVO.app",
  "Windows": "C:/Program Files/Audient/EVO/EVO.exe"
}

@pytest.fixture(scope="session", autouse=True)
def AppName() -> str:
    return "EVO"

@pytest.fixture(scope="session", autouse=True)
def AppPath() -> str:
    if system() in app_paths:
        return app_paths[system()]
    else:
        raise NotImplementedError("The current OS is not currently supported: " + system())
    
@pytest.fixture(scope="session", autouse=True)
def Application(AppName, AppPath) -> UIApplication:
    app = UIApplication(appName=AppName, appPath=AppPath)
    app.launchApp()
    app.connectApp()

    yield app

    # app.terminateApp()

@pytest.fixture(scope="session", autouse=True)
def MainWindow(Application) -> UIWindow:
    return Application.window(title="EVO Mixer", timeout = 2)


def test_version():
    assert __version__ == '0.1.0'

# @pytest.mark.skipif(condition=(system() != "Darwin"), reason="MacOS specific tests")
@pytest.mark.usefixtures("MainWindow")
class TestMacOS():

    def test_button_click(self, MainWindow):
        button = MainWindow.findR(title = f"Mic 1 polarity", control_type = UIButton)
        button.click()
        button.click()
    
    def test_button_press(self, MainWindow):
        button = MainWindow.findR(title = f"Mic 1 solo", control_type = UIButton)
        
        button.press()
        button.press()
    
    # def test_hotkeys(self, MainWindow):
    #     shortcut = ("ctrl", "alt", "b") if (system() != "Darwin") else ("option", "command", "b")
    #     hotkey(*shortcut, interval=0.01)

    #     button = MainWindow.findR(description = "Close Secondary Side Bar", control_type = UIButton, timeout=2)
    #     hotkey(*shortcut, interval=0.01)
    #     assert True

        
    # def test_button_click(self, MainWindow):
    #     MainWindow.findR(title = "Sound", control_type = UIButton).click()
    
    # def test_slider(self, MainWindow):
    #     MainWindow.findR(control_type = UISlider).setValue(0)
    #     currentValue = MainWindow.findR(control_type = UISlider).getValue()
    #     MainWindow.findR(control_type = UISlider).setValue(0.5)

    #     assert currentValue == 0
        
    # def test_hotkeys(self, MainWindow):
    #     pass#hotkey("command", "t", interval=0.01)
    

