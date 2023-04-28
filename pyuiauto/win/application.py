#___MY_MODULES___
from pyuiauto.win.components import UIBaseComponent, UIWindow
from pyuiauto.base.application import UIApplicationWrapper
from pyuiauto.exceptions import ElementNotFound, WindowNotFound

#___MODULES___
from typing import Type

# pip installed modules
try:
        import pywinauto
        from pywinauto.application import process_get_modules
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')

#___DEFINING_NATIVE_METHODS___
class UIApplication(UIApplicationWrapper):

    def launchApp(self) -> None:
        pywinauto.Application().start(self.appPath)
    
    def connectApp(self) -> None:
        self._app = pywinauto.Application(backend="uia", allow_magic_lookup=False).connect(title=self.appName, path=f"{self.appName}.exe")
    
    def terminateApp(self) -> None:
        self._app.kill()
    
    def window(self, timeout: int = 1, retry_interval: float = 0.1, **criteria):
        try:
            window = self._app.window(**criteria)
            window.wait('exists', timeout=timeout, retry_interval=retry_interval)
            return UIWindow(window.wrapper_object())
        except pywinauto.timings.TimeoutError:
             raise WindowNotFound
    
    def windows(self, timeout: int = 1, retry_interval: float = 0.1, **criteria):
        try:
            windows = list(UIWindow(window) for window in self._app.windows(**criteria))
            if len(windows) == 0:
                raise WindowNotFound
        except pywinauto.timings.TimeoutError:
             raise WindowNotFound
    
    def isAppAlreadyRunning(self):
        for module in process_get_modules():
            if self.appPath == module[1]:
                 return True
        return False

    def isAppRunning(self):
        return self._app.is_process_running()