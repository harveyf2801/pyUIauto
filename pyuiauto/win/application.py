#___MODULES___
from __future__ import annotations
from typing import Type
import datetime
import subprocess

# pip installed modules
try:
        import pywinauto
        from pywinauto.application import process_get_modules
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')

#___MY_MODULES___
from pywinauto.controls.uiawrapper import UIAWrapper
from pyuiauto.win.components import UIBaseComponent, UIWindow, UIButton
from pyuiauto.base.application import UIApplicationWrapper, UISystemTrayIconWrapper
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
        return UIButton(parent.child_window(title_re=f".*of.*{self.app.appName}", control_type="Button", found_index=0).wrapper_object())

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
        if self.__systrayExpandWindow.is_visible():
            backendExplorer.taskbarExpand.invoke()
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



#___DEFINING_NATIVE_METHODS___
class UIApplication(UIApplicationWrapper):

    def launchApp(self) -> None:
        pywinauto.Application().start(self.appPath)
    
    def connectApp(self) -> None:
        self._app = pywinauto.Application(backend="uia", allow_magic_lookup=False).connect(title=self.appName, path=f"{self.appName}.exe")
    
    def terminateApp(self) -> None:
        self._app.kill()
    
    def window(self, timeout: int = 1, retry_interval: float = 0.1, **criteria) -> UIWindow:
        try:
            window = self._app.window(**criteria)
            window.wait('exists', timeout=timeout, retry_interval=retry_interval)
            return UIWindow(window.wrapper_object())
        except pywinauto.timings.TimeoutError:
             raise WindowNotFound
    
    def windows(self, timeout: int = 1, retry_interval: float = 0.1, **criteria) -> list[UIWindow]:
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

    def getSystemTrayIcon(self):
        return UISystemTrayIcon(self)
    
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