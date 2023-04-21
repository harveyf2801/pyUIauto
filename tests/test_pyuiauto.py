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

    app.terminateApp()

@pytest.fixture(scope="session", autouse=True)
def MainWindow(Application) -> UIWindow:
    return Application.window(title="EVO Mixer", timeout = 2)


def test_version():
    assert __version__ == '0.1.0'

import time
# @pytest.mark.skipif(condition=(system() != "Darwin"), reason="MacOS specific tests")
@pytest.mark.usefixtures("MainWindow")
class TestMacOS():

    def test_button_click(self, MainWindow):
        MainWindow.setFocus()
        button = MainWindow.findR(title = f"Mic 1 polarity", control_type = UIButton)
        previous = button.getValue()
        button.click()
        current = button.getValue()

        if previous == current:
            assert False
        else:
            button.click()
            assert True
    
    def test_button_press(self, MainWindow):
        button = MainWindow.findR(title = f"Mic 1 solo", control_type = UIButton)
        previous = button.getValue()
        button.press()
        current = button.getValue()

        if previous == current:
            assert False
        else:
            button.press()
            assert True
    
    def test_slider_value(self, MainWindow):
        slider = MainWindow.findR(title = f"Mic 1 fader", control_type = UISlider)
        previous = slider.getValue()
        slider.setValue(0 if previous != 0 else -128)
        current = slider.getValue()

        if previous == current:
            assert False
        else:
            slider.setValue(previous)
            assert True
        
    def test_hotkeys(self, Application):
        hotkey("ctrl", "4", interval=0.01)
        try: 
            system_panel = Application.window(title="SYSTEM PANEL", timeout=2)
            system_panel.close()
            assert True
        except WindowsError:
            assert False

