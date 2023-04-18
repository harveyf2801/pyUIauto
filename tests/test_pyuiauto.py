from platform import system
import os
import pytest

from pyuiauto.src.application import UIApplication
from pyuiauto.src.components import UIWindow, UIButton
from pyuiauto import __version__

app_paths = {
  "Darwin": "/Applications/Visual Studio Code.app",
  "Windows": os.path.expanduser('~') + "\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}

@pytest.fixture()
def AppPath() -> str:
    if system() in app_paths:
        return app_paths[system()]
    else:
        raise NotImplementedError("The current OS is not currently supported: " + system())
    
@pytest.fixture()
def Application() -> UIApplication:
    app = UIApplication(appName="Visual Studio Code", appPath=app_paths[system()])
    app.launchApp()
    app.connectApp()

    yield app

    app.terminateApp()


def test_version():
    assert __version__ == '0.1.0'


class ComponentTests():
    main_window: UIWindow

    def test_window(self, Application):
        ComponentTests.main_window = Application.window(title = "Visual Studio Code", timeout = 2)
    
    def test_button_toggle_press(self):
        button1 = ComponentTests.main_window.findR(title = "Toggle Primary Side Bar (Ctrl+B)", control_type = UIButton)
        button1.toggle(value=1)
        assert button1.getValue() == 1

    def test_button_click(self):
        button2 = ComponentTests.main_window.findR(title = "Toggle Panel (Ctrl+J)", control_type = UIButton)
        current_value = button2.getValue()
        button2.click()
        assert button2.getValue() != current_value


