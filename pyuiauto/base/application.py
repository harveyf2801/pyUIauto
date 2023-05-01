# ___MODULES___
from __future__ import annotations
import time
from abc import ABC, abstractmethod
import logging

# __MY_MODULES__
from pyuiauto.base.components import UIWindowWrapper, UIButtonWrapper
from pyuiauto.exceptions import ProcessNotFoundError


# ___CLASSES___

class UISystemTrayIconWrapper(ABC):
    def __init__(self, app: UIApplicationWrapper):
        self.app = app

    @abstractmethod
    def __enter__(self) -> UIButtonWrapper:
        'Using a context manager helps to creates the UIButton dynamically.'
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
    def window(self, timeout: int = 1, retry_interval: float = 0.1, **criteria) -> UIWindowWrapper:
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
    def windows(self, timeout: int = 1, retry_interval: float = 0.1, **criteria) -> list[UIWindowWrapper]:
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
    def getCrashReport(self) -> str:
        '''Application class get crash report method\n
        Gets all crash reports between the start and end time of the application running.'''

    def relaunchApp(self):
        '''Application class relaunch app method\n
        Uses it's context manager __enter__ __exit__ methods to quit and reopen the application.'''
        self.__exit__()
        self.launchApp()
        self.__enter__()

    def __enter__(self):
        self.launchApp()
        self.connectApp()
        return self
    
    def __exit__(self, *args):
        if not self.isAppRunning():
            logging.critical(f"The {self.appName} application may have crashed")
            logging.error(f"Crash report:\n{self.getCrashReport()}")
            raise ProcessNotFoundError(f"The {self.appName} application was not found in running applications")
        else:
            self.terminateApp()
