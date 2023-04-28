# __MY_MODULES__
from pyuiauto.base.components import UIWindowWrapper

# ___MODULES___
from abc import ABC, abstractmethod


# ___CLASSES___

class UIApplicationWrapper(ABC):
    def __init__(self, appName: str, appPath: str = None) -> None:
        self.appName = appName
        self.appPath = appPath

    @abstractmethod
    def launchApp(self) -> None:
        '''Application class launch app method\n
        Launches the application.'''

    @abstractmethod
    def connectApp(self) -> None:
        '''Application class connect app method\n
        Connects the application wrapper to the specfied running app.'''

    @abstractmethod
    def terminateApp(self) -> None:
        '''Application class terminate app method\n
        Force quits the application.'''
    
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
