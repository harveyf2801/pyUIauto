import pytest
from platform import system
import time

from pyuiauto.application import UIApplication
from pyuiauto.components import UIWindow, UIMenuBarItem
from pyautogui import hotkey, write, press

@pytest.mark.skipif(condition=(system() != "Windows"), reason="Skipping Windows tests")
class TestWindows():

        @pytest.fixture(scope="session", autouse=True)
        def Application(self) -> UIApplication:
                app = UIApplication(appName="Notepad", appPath="Notepad.exe")
                
                if not app.isAppAlreadyRunning():
                        app.launchApp()

                app.connectApp()
                assert app.isAppRunning(), "UIApplication failed to launch correctly"
                yield app
                app.terminateApp()

        @pytest.fixture(scope="session", autouse=True)
        def MainWindow(self, Application: UIApplication):
                main_window = Application.window(title="Notepad", timeout=2) # getting all windows (with no criteria) and selecting the first one
                main_window.setFocus()
                assert main_window.isVisible(), "UIWindow.setFocus() failed"

                yield main_window

                main_window.close()

        def test_typing(self, MainWindow: UIWindow):
                write("12345")
                hotkey("ctrl", "A", interval=0.01)
                press("del")
                
        def test_menu_bar(self, Application: UIApplication, MainWindow: UIWindow):
                MainWindow.findFirstR(title="File", control_type=UIMenuBarItem).click()
                try: MainWindow.findFirstR(title="New window", control_type=UIMenuBarItem).invoke()
                except: assert False, "UIMenuBarItem.click() failed"

                time.sleep(1)
                all_windows = Application.windows(title="Notepad")
                assert len(all_windows) == 2, "UIMenuBarItem.invoke() failed"

                all_windows[0].close()
        
        @pytest.mark.xfail(reason="Not all UIComponents have been implemented yet")
        def test_components(self, MainWindow: UIWindow):
                all_children = MainWindow.getChildren()
