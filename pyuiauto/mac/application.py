#___MODULES___
from __future__ import annotations
from typing import Type
import os
import datetime
import logging
import contextlib
from typing import Union

# pip installed modules
try:
        import atomacos
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install atomacos (MacOS ONLY)')

try:
    from pyautogui import press
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pyautogui')


#___MY_MODULES___
from pyuiauto.mac.components import UIBaseComponent, UIWindow, UIButton, UIMenuBarItem, UIMenuItem
from pyuiauto.base.application import UIApplicationWrapper, UIPopupMenuWrapper, UISystemTrayIconWrapper, UIPopupMenuWrapper
from pyuiauto.exceptions import ElementNotFound, WindowNotFound


class UISystemTrayIcon(UISystemTrayIconWrapper):
    def __init__(self, app: UIApplicationWrapper):
        super().__init__(app)

    def __enter__(self) -> UIMenuBarItem:
        return self.app._findFirstR(control_type=UIMenuBarItem, AXSubrole="AXMenuExtra")
    
    def __exit__(self, *args):
        pass

class UIPopupMenu(UIPopupMenuWrapper):
    def __init__(self, app: UIApplicationWrapper, popup_naming_scheme: str = None) -> None:
        super().__init__(app, popup_naming_scheme)

    def getMenuItemFromPath(self, *path: str) -> UIMenuItem:
        current_item = None

        for count, i in enumerate(path):
            self.current_popup = self.app.window(title=self.win_name)
            current_item = self.current_popup.findFirstR(title=i, control_type=UIMenuItem)
            if count == len(path)-1:
                current_item.invoke()
            self.steps += 1
        
        return current_item
    
    def _nativeMenuBarItemFromPath(self, *path: str) -> UIMenuBarItem:
        current_item = UIMenuItem(self.app._app.menuItem(*path))
        self.steps = len(path)
        
        return current_item
        
    def back(self):
        if self.steps > 0:
            press("left")
            self.steps -= 1

    def backToRoot(self):
        for i in range(self.steps):
            press("left")
            self.steps -= 1
    
    def __enter__(self) -> UIPopupMenu:
        return self
        
    def __exit__(self, *args) -> None:
        if self.current_popup != None and self.current_popup.exists():
            press("esc")


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

    def getPopupMenu(self, popup_naming_scheme: str = None) -> UIPopupMenu:
        return UIPopupMenu(self, popup_naming_scheme)
    
    def getSystemTrayIcon(self) -> UISystemTrayIcon:
        return UISystemTrayIcon(self)
    
    @contextlib.contextmanager
    def systemTrayPopupPath(self, *path: str) -> UIMenuItem:
        with self.getSystemTrayIcon() as icon:
            icon.right_click()
        
            with self.getPopupMenu() as popup:
                try:

                    yield popup.getMenuItemFromPath(*path)
                except ElementNotFound:
                    raise ElementNotFound(f"{path} is disabled or not available")
    
    @contextlib.contextmanager
    def menuBarPopupPath(self, window: UIWindow, *path: str) -> Union[UIMenuBarItem, UIMenuItem]:
        try:
            menuBarItem = self._findFirstR(title=path[0], control_type=UIMenuBarItem)
            if len(path) == 1:
                yield menuBarItem
            
            with self.getPopupMenu(popup_naming_scheme="") as popup:
                yield popup._nativeMenuBarItemFromPath(*path)
        
        except ElementNotFound:
                    raise ElementNotFound(f"{path} is disabled or not available")