#___MODULES___
from __future__ import annotations
from typing import Type
import datetime
import subprocess
import logging
import contextlib
from typing import Union

# pip installed modules
try:
        import pywinauto
        from pywinauto.application import process_get_modules
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')

try:
    from pyautogui import press
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pyautogui')


#___MY_MODULES___
from pywinauto.controls.uiawrapper import UIAWrapper
from pyuiauto.win.components import UIBaseComponent, UIWindow, UIButton, UIMenuItem, UIMenuBarItem
from pyuiauto.base.application import UIApplicationWrapper, UISystemTrayIconWrapper, UIPopupMenuWrapper
from pyuiauto.exceptions import ElementNotFound, WindowNotFound

class UIBackendExplorer():
    backend_explorer_app = pywinauto.Application(backend="uia").connect(path="explorer.exe")
    backend_explorer_app = pywinauto.Application(backend="uia").connect(path="explorer.exe")
    taskbar: pywinauto.WindowSpecification = backend_explorer_app.window(title="Taskbar", class_name="Shell_TrayWnd")

    try:
        taskbarExpand = UIButton(taskbar.child_window(title="Show Hidden Icons", class_name="SystemTray.NormalButton").wrapper_object())
    except:
        try:
            taskbarExpand = UIButton(taskbar.child_window(title="Notification Chevron").wrapper_object())
        except:
            raise ElementNotFound("Show Hidden Icons not found.")
        
backendExplorer = UIBackendExplorer()

class UISystemTrayIcon(UISystemTrayIconWrapper):
    def __init__(self, app: UIApplicationWrapper):
        super().__init__(app)

        self._iconHidden = False
        
        try:
            self._getIcon(backendExplorer.taskbar)
        except:
                self.__systrayExpandWindow = None
                self._iconHidden = True
    
    def _getIcon(self, parent: pywinauto.WindowSpecification) -> UIButton:
        icon = parent.child_window(title_re=f".*{self.app.appName}", control_type="Button", class_name="SystemTray.NormalButton", found_index=0)
        icon.wait('exists', timeout=2)
        icon.wrapper_object()
        return UIButton(icon)

    def __openSystemTrayExpand(self) -> pywinauto.WindowSpecification:
        # Open the system tray
        backendExplorer.taskbarExpand.invoke()

        # Select the audient icon
        try:
            systray = pywinauto.Application(backend="uia").connect(class_name="TopLevelWindowForOverflowXamlIsland")
            systrayWindow = systray.window(class_name="TopLevelWindowForOverflowXamlIsland")
            
        except:
            try:
                systray = pywinauto.Application(backend="uia").connect(class_name="NotifyIconOverflowWindow")
                systrayWindow = systray.window(class_name="NotifyIconOverflowWindow")
                
            except:
                raise WindowNotFound("Notification Overflow Window not found.")

        systrayWindow.wait("visible")
        return systrayWindow

    def __closeNotifictionExpand(self) -> None:
        # Close the system tray
        if self.__systrayExpandWindow.exists() and self.__systrayExpandWindow.is_visible():
            backendExplorer.taskbarExpand.invoke() # pyautogui.press("esc") will also work for closing popup menu windows
            self.__systrayExpandWindow.wait_not("visible")

    def __enter__(self) -> UIButton:
        if self._iconHidden:
            try:
                self.__systrayExpandWindow = self.__openSystemTrayExpand()
                return self._getIcon(self.__systrayExpandWindow)
            except: raise ElementNotFound("System Tray Icon not found.")
        
        return self._getIcon(backendExplorer.taskbar)
    
    def __exit__(self, *args):
        if self._iconHidden:
            self.__closeNotifictionExpand()


class UIPopupMenu(UIPopupMenuWrapper):
    def __init__(self, app: UIApplicationWrapper, popup_naming_scheme: str = None) -> None:
        super().__init__(app, popup_naming_scheme)

    def getMenuItemFromPath(self, *path: str) -> UIMenuItem:
        current_item = None

        for count, i in enumerate(path):
            self.current_popup = self.app.window(title=self.win_name, found_index=0)
            current_item = self.current_popup.findFirstR(title=i, control_type=UIMenuItem)
            if count == len(path)-1:
                current_item.invoke()
            self.steps += 1
        
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
        if self.current_popup.isVisible():
            press("esc")


#___DEFINING_NATIVE_METHODS___
class UIApplication(UIApplicationWrapper):

    def launchApp(self) -> None:
        pywinauto.Application().start(self.appPath)
    
    def connectApp(self) -> None:
        self._app = pywinauto.Application(backend="uia", allow_magic_lookup=False).connect(title=self.appName, path=self.appPath)
    
    def terminateApp(self) -> None:
        self._app.kill()
    
    def window(self, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> UIWindow:
        try:
            window = self._app.window(**criteria)
            window.wait('exists', timeout=timeout, retry_interval=retry_interval)
            return UIWindow(window.wrapper_object())
        except pywinauto.timings.TimeoutError:
             raise WindowNotFound
    
    def windows(self, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> list[UIWindow]:
        try:
            windows = list(UIWindow(window) for window in self._app.windows(**criteria))
            if len(windows) == 0:
                raise WindowNotFound
            return windows
        except pywinauto.timings.TimeoutError:
             raise WindowNotFound
    
    def isAppAlreadyRunning(self):
        for module in process_get_modules():
            if self.appPath == module[1]:
                 return True
        return False

    def isAppRunning(self):
        return self._app.is_process_running()
    
    def getCrashReport(self):
        # Convert epoch timestamp to a datetime object
        start_datetime = datetime.datetime.fromtimestamp(self.start_time)
        end_datetime = datetime.datetime.fromtimestamp(self.end_time)

        # Format datetime object as a string in the required format
        start_time = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        end_time = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        command = f"powershell.exe Get-WinEvent -FilterHashtable @{{Logname='Application';Data='{self.appName}';StartTime='{start_time}';EndTime='{end_time}'}}"
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    
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
            menuBarItem = window.findFirstR(title=path[0], control_type=UIMenuBarItem)
            if len(path) == 1:
                yield menuBarItem
            
            menuBarItem.click()
            with self.getPopupMenu() as popup:
                yield popup.getMenuItemFromPath(*path[1:])
        
        except ElementNotFound:
                    raise ElementNotFound(f"{path} is disabled or not available")