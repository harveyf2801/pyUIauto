#___MY_MODULES___
from pyuiauto.src.mac.components import UIBaseComponent, UIWindow
from pyuiauto.src.base.application import UIApplicationWrapper
from pyuiauto.src.exceptions import ElementNotFound, WindowNotFound

#___MODULES___
from typing import Type

# pip installed modules
try:
        import atomacos
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install atomacos (MacOS ONLY)')

#___DEFINING_NATIVE_METHODS___

class UIApplication(UIApplicationWrapper):

    def launchApp(self) -> None:
        atomacos.launchAppByBundlePath(self.appPath)
    
    def connectApp(self) -> None:
        self._app = atomacos.getAppRefByLocalizedName(self.appName)
        self._app.activate()
        self._bundleID = self._app.getBundleId()
    
    def terminateApp(self) -> None:
        atomacos.terminateAppByBundleId(self._bundleID)
    
    def _findAll(self, control_type: Type[UIBaseComponent], **options):
        return UIBaseComponent(self._app).findAll(
                                                    control_type=control_type,
                                                    **options)
    
    def _findFirst(self, control_type: Type[UIBaseComponent], **options):
        return UIBaseComponent(self._app).findFirst(
                                                    control_type=control_type,
                                                    **options)
    
    def _findFirstR(self, control_type: Type[UIBaseComponent], **options):
        return UIBaseComponent(self._app).findFirstR(
                                                    control_type=control_type,
                                                    **options)
    
    def _findAllR(self, control_type: Type[UIBaseComponent], **options):
        return UIBaseComponent(self._app).findAllR(
                                                    control_type=control_type,
                                                    **options)
    
    def _find(self, control_type: Type[UIBaseComponent], **options):
        return UIBaseComponent(self._app).find(
                                                    control_type=control_type,
                                                    **options)

    def _findR(self, control_type: Type[UIBaseComponent], **options):
        return UIBaseComponent(self._app).findR(
                                                    control_type=control_type,
                                                    **options)

    def window(self, timeout: int = 1, retry_interval: float = 0.1, **options) -> UIWindow:
        try:
            return self.windows(timeout=timeout, retry_interval=retry_interval, **options)[-1]
        except ElementNotFound:
             raise WindowNotFound
    
    def windows(self, timeout: int = 1, retry_interval: float = 0.1, **options) -> list[UIWindow]:
        try:
            return self._findAllR(control_type=UIWindow, timeout=timeout, retry_interval=retry_interval, **options)
        except ElementNotFound:
             raise WindowNotFound
    
    def isAppAlreadyRunning(self):
        for i in atomacos.NativeUIElement.getRunningApps():
            if self.appPath in str(i.executableURL()):
                return True
        return False
    
    def isAppRunning(self):
        return atomacos.NativeUIElement._running_app
