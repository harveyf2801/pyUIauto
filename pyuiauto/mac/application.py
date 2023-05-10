#___MODULES___
from typing import Type
import os
import datetime
import logging

# pip installed modules
try:
        import atomacos
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install atomacos (MacOS ONLY)')


#___MY_MODULES___
from pyuiauto.mac.components import UIBaseComponent, UIWindow, UIButton, UIMenuBarItem
from pyuiauto.base.application import UIApplicationWrapper, UISystemTrayIconWrapper
from pyuiauto.exceptions import ElementNotFound, WindowNotFound


class UISystemTrayIcon(UISystemTrayIconWrapper):
    def __init__(self, app: UIApplicationWrapper):
        super().__init__(app)

    def __enter__(self) -> UIButton:        
        return UIButton(self.app._findFirstR(control_type=UIMenuBarItem, AXSubrole="AXMenuExtra"))
    
    def __exit__(self, *args):
        pass

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

    def window(self, timeout: int = 1, retry_interval: float = 0.01, **options) -> UIWindow:
        try:
            return self.windows(timeout=timeout, retry_interval=retry_interval, **options)[-1]
        except ElementNotFound:
             raise WindowNotFound
    
    def windows(self, timeout: int = 1, retry_interval: float = 0.01, **options) -> list[UIWindow]:
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
    
    def getSystemTrayIcon(self):
        return UISystemTrayIcon(self) # AXSubRole is MacOS ONLY criteria

    def getCrashReport(self):
        diagnostic_reports_path = os.path.join(os.path.expanduser('~'), "Library", "Logs", "DiagnosticReports")

        for file in os.listdir(diagnostic_reports_path):
            if file.endswith(".ips"):
                app, year, month, date, time_ = file.split("-")
                time_ = time_.split(".")[0]

                if app == self.appName:

                    file_time = datetime.datetime(int(year), int(month), int(date), int(time_[:2]), int(time_[2:4]), int(time_[4:]))
                    start_time = datetime.datetime.fromtimestamp(self.start_time)
                    end_time = datetime.datetime.fromtimestamp(self.end_time)
                    
                    logging.debug(f"Start Time: {start_time}, End Time: {end_time}, File Time: {file_time}")
                    
                    
                    if ( (start_time <= file_time) and (end_time >= file_time) ):
                        return os.path.join(diagnostic_reports_path, file)