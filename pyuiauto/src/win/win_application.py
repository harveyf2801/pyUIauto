#___MY_MODULES___
from src.drivers.appautomation.cross_automation_component import UIWindowWrapper, UIMenuItemWrapper
from src.drivers.appautomation.cross_automation_exceptions import UIElementNotFoundError, UIWindowNotFoundError

#___MODULES___
from typing import Type

# pip installed modules
try:
        import pywinauto
        from pywinauto.application import process_get_modules
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')


#___DEFINING_NATIVE_METHODS___
class _UIApplication():

    def launchApp(self) -> None:
        pywinauto.Application().start(self.appPath)
    
    def connectApp(self) -> None:
        self._app = pywinauto.Application(backend="uia", allow_magic_lookup=False).connect(title=self.appName, path=self.appPath)
    
    def terminateApp(self) -> None:
        self._app.kill()
    
    def window(self, timeout: int = 1, retry_interval: float = 0.1, **criteria):
        try:
            window = self._app.window(**criteria)
            window.wait('exists', timeout=timeout, retry_interval=retry_interval)
            return UIWindowWrapper(window.wrapper_object())
        except pywinauto.timings.TimeoutError:
             raise UIWindowNotFoundError
    
    def windows(self, timeout: int = 1, retry_interval: float = 0.1, **criteria):
        try:
            return list(UIWindowWrapper(window) for window in self._app.windows(**criteria))
        except pywinauto.timings.TimeoutError:
             raise UIWindowNotFoundError
    
    def isAppAlreadyRunning(self):
        for module in process_get_modules():
            if self.appPath == module[1]:
                 return True
        return False

    def isAppRunning(self):
        return self._app.is_process_running()