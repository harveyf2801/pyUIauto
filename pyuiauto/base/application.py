# ___MODULES___
from __future__ import annotations
import time
from abc import ABC, abstractmethod
import logging
import contextlib
from typing import Union

try:
    from pyautogui import press
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pyautogui')

# __MY_MODULES__
from pyuiauto.components import UIWindow, UIButton, UIMenuItem, UIMenuBarItem
from pyuiauto.exceptions import ProcessNotFoundError, ElementNotFound


# ___CLASSES___

class UISystemTrayIconWrapper(ABC):
    '''UISystemTrayIconWrapper\n
    Provides a system tray icon manager to help find the system tray icon for an application\n
    whether it be hidden within the notification expand window or on the taskbar.'''
    def __init__(self, app: UIApplicationWrapper):
        self.app = app

    @abstractmethod
    def __enter__(self) -> UIButton:
        'Using a context manager helps to creates the UIButton dynamically.'

    @abstractmethod
    def __exit__(self, *args) -> None:
        'Using a context manager helps to dynamically tidy any open windows.'
    
    
class UIPopupMenuWrapper(ABC):
    '''UIPopupMenuWrapper\n
    Provides a popup manager for popup windows to help select specific menu item\n
    and provides a cleanup of popup windows.\n
    
    The popup_naming_scheme can vary from app to app however, these are some examples:\n
        - *the application name*\n
        - "Context"
        - "Pop-up"
    '''
    def __init__(self, app: UIApplicationWrapper, popup_naming_scheme: str = None) -> None:
        self.app = app
        self.win_name = popup_naming_scheme if popup_naming_scheme else app.appName
        self.current_popup = None
        self.steps = 0

    @abstractmethod
    def getMenuItemFromPath(self, *path: str) -> UIMenuItem:
        '''PopupMenu class get menu item from path method\n
        Uses the specified path to return a menu item component at [-1] index of the path.'''
    
    @abstractmethod
    def back(self):
        'Go back a popup menu window to the previous item'

    @abstractmethod
    def backToRoot(self):
        'Go back to the root popup menu window'
    
    @abstractmethod
    def __enter__(self) -> UIPopupMenuWrapper:
        'Using a context manager helps to creates the popup windows dynamically.'
    
    @abstractmethod
    def __exit__(self, *args) -> None:
        'Using a context manager helps to dynamically tidy any open windows.'


class UIApplicationWrapper(ABC):
    def __init__(self, appName: str, appPath: str = None) -> None:
        self.appName = appName
        self.appPath = appPath
        self.end_time = 0
        self.start_time = 0

    @abstractmethod
    def launchApp(self) -> None:
        '''Application class launch app method\n
        Launches the application.'''
        self.start_time = time.time()

    @abstractmethod
    def connectApp(self) -> None:
        '''Application class connect app method\n
        Connects the application wrapper to the specfied running app.'''

    @abstractmethod
    def terminateApp(self) -> None:
        '''Application class terminate app method\n
        Force quits the application.'''
        self.end_time = time.time()
    
    def getRuntime(self):
        return self.end_time - self.start_time
    
    @abstractmethod
    def window(self, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> UIWindow:
        '''Application class window method\n
        Finds a window child component with the specified criteria.
        Raises an exception if the criteria matches no components (recursive).\n
        Args:                    
                    (criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    component: window component wrapped to it's cross compatible custom wrapper of type UIWindowWrapper'''
    
    @abstractmethod
    def windows(self, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> list[UIWindow]:
        '''Application class windows method\n
        Finds all window child components with the specified criteria.
        Raises an exception if the criteria matches > 1 or no components (recursive).\n
        Args:                    
                    (criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    components: window components wrapped to it's cross compatible custom wrapper in a list of type UIWindowWrapper'''

    @abstractmethod
    def isAppAlreadyRunning(self) -> bool:
        '''Application class is app already running method\n
        This method checks if the application name is found in already running instances.'''

    @abstractmethod
    def isAppRunning(self) -> bool:
        '''Application class is app running method\n
        This method checks if the application is still running which can help to identify crashes.'''

    @abstractmethod
    def getSystemTrayIcon(self) -> UISystemTrayIconWrapper:
        '''Application class get system tray icon method\n
        Returns the system tray icon button component wrapper.\n
        (a context manager is required to interact with this component)\n
        Example:\n
        with UISystemTrayIcon() as icon:
            icon.right_click()
            ...'''
    
    @abstractmethod
    def getPopupMenu(self, popup_naming_scheme: str = None) -> UIPopupMenuWrapper:
        '''Application class get popup menu method\n
        Returns the popup menu component wrapper.\n
        (a context manager is required to interact with this component)\n
        Example:\n
        with UIPopupMenuWrapper() as popup:
            item = popup.getMenuItemFromPath("Setup", "Set Sample Rate", "96kHz")
            ...\n
        
        The popup_naming_scheme can vary from app to app however, these are some examples:\n
        - *the application name* (default)
        - "Context"
        - "Pop-up"
        '''

    @abstractmethod
    def systemTrayPopupPath(self, *path: str) -> UIMenuItem:
        '''Application class system tray popup select method\n
        This method selects menu items after clicking the system tray, from the *args passed in as a path.'''
    
    @abstractmethod
    def menuBarPopupPath(self, window: UIWindow, *path: str) -> Union[UIMenuBarItem, UIMenuItem]:
        '''Application class menu bar select method\n
        This method selects menu items on the menubar from the *args passed in as a path.'''

    @abstractmethod
    def getCrashReport(self) -> str:
        '''Application class get crash report method\n
        Gets all crash reports between the start and end time of the application running.'''

    def relaunchApp(self):
        '''Application class relaunch app method\n
        Uses it's context manager __enter__ __exit__ methods to quit and reopen the application.'''
        self.__exit__()
        time.sleep(0.5)
        self.__enter__()

    def __enter__(self) -> UIApplicationWrapper:
        self.launchApp()
        self.connectApp()
        return self
    
    def __exit__(self, *args):
        if not self.isAppRunning():
            logging.warning(f"The {self.appName} application may have crashed as it was not found in running applications")
            # logging.error(f"Crash report:\n{self.getCrashReport()}")
            # raise ProcessNotFoundError(f"The {self.appName} application was not found in running applications")
        else:
            self.terminateApp()
