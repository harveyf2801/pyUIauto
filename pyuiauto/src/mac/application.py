#___MY_MODULES___
from pyuiauto.src.components import UIBaseComponentWrapper, UIWindowWrapper
from pyuiauto.src.application import UIApplicationWrapper
from pyuiauto.src.exceptions import ElementNotFound, WindowtNotFound

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
    
    def _findAll(self, control_type: Type[UIBaseComponentWrapper], **options):
        return UIBaseComponentWrapper(self._app).findAll(
                                                    control_type=control_type,
                                                    **options)
    
    def _findFirst(self, control_type: Type[UIBaseComponentWrapper], **options):
        return UIBaseComponentWrapper(self._app).findFirst(
                                                    control_type=control_type,
                                                    **options)
    
    def _findFirstR(self, control_type: Type[UIBaseComponentWrapper], **options):
        return UIBaseComponentWrapper(self._app).findFirstR(
                                                    control_type=control_type,
                                                    **options)
    
    def _findAllR(self, control_type: Type[UIBaseComponentWrapper], **options):
        return UIBaseComponentWrapper(self._app).findAllR(
                                                    control_type=control_type,
                                                    **options)
    
    def _find(self, control_type: Type[UIBaseComponentWrapper], **options):
        return UIBaseComponentWrapper(self._app).find(
                                                    control_type=control_type,
                                                    **options)

    def _findR(self, control_type: Type[UIBaseComponentWrapper], **options):
        return UIBaseComponentWrapper(self._app).findR(
                                                    control_type=control_type,
                                                    **options)

    def window(self, timeout: int = 1, retry_interval: float = 0.1, **options):
        try:
            return self.windows(timeout, retry_interval, **options)[-1]
        except ElementNotFound:
             raise WindowtNotFound
    
    def windows(self, timeout: int = 1, retry_interval: float = 0.1, **options):
        try:
            return self._findAllR(timeout=timeout, retry_interval=retry_interval,
                        control_type=UIWindowWrapper,
                        **options)
        except ElementNotFound:
             raise WindowtNotFound
    
    def isAppAlreadyRunning(self):
        for i in atomacos.NativeUIElement.getRunningApps():
            if self.appPath in str(i.executableURL()):
                return True
        return False
    
    def isAppRunning(self):
        return atomacos.NativeUIElement._running_app
