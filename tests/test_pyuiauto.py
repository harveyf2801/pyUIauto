from platform import system
import os
import pytest

from pyuiauto.src.application import UIApplication
from pyuiauto.src.components import UIWindow, UIButton, UISlider
from pyuiauto import __version__

from pyautogui import hotkey

app_paths = {
  "Darwin": "/System/Applications/System Preferences.app",
  "Windows": "c:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
}

@pytest.fixture(scope="session", autouse=True)
def AppName() -> str:
    return "System Preferences" if system() == "Darwin" else "Notepad"

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

    #app.terminateApp()

@pytest.fixture(scope="session", autouse=True)
def MainWindow(Application) -> UIWindow:
    return Application.window(timeout = 2)


def test_version():
    assert __version__ == '0.1.0'

@pytest.mark.usefixtures("MainWindow")
@pytest.mark.skipif(condition=(system() != "Darwin"), reason="MacOS specific tests")
class TestMacOS():

    def test_button_press(self, MainWindow):
        MainWindow.findR(description = "Show All", control_type = UIButton).press()
    
    def test_button_click(self, MainWindow):
        MainWindow.findR(title = "Sound", control_type = UIButton).click()
    
    def test_slider(self, MainWindow):
        MainWindow.findR(control_type = UISlider).setValue(0)
        currentValue = MainWindow.findR(control_type = UISlider).getValue()
        MainWindow.findR(control_type = UISlider).setValue(0.5)

        assert currentValue == 0
        
    

    def test_hotkeys(self, MainWindow):
        pass#hotkey("command", "t", interval=0.01)
    

