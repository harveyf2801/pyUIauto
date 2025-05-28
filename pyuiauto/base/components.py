# ___MODULES___
from __future__ import annotations
from abc import ABC, ABCMeta, abstractmethod
from typing import Type, Union

# ___CLASSES___

class UIBaseComponentWrapperMeta(ABCMeta):
    """Metaclass for UIComponentWrapper objects"""

    control_type_to_cls = {}

    def __init__(cls, name, bases, attrs):
        """Register the control types"""

        if name != "UIBaseComponentWrapper":
            UIBaseComponentWrapperMeta.control_type_to_cls[cls.native_control_type] = cls

    @staticmethod
    def find_wrapper(component):
        """Find the correct wrapper for this UIA component"""
        raise NotImplementedError

class UIBaseComponentWrapper(object, metaclass=UIBaseComponentWrapperMeta):
    """
    Abstract / Default wrapper for User Interface controls.

    All other UI wrappers are derived from this.

    This class wraps a lot of functionality of underlying UI features
    for working with Mac or Windows.

    Most of the methods apply to every single component type. For example
    you can click() on any component.

    """
    
    def __new__(cls, component):
        return UIBaseComponentWrapper._create_wrapper(cls, component, UIBaseComponentWrapper)
    
    @staticmethod
    def _create_wrapper(cls_spec, component, myself):
        """Create a wrapper object according to the specified component"""
        # only use the meta class to find the wrapper for BaseWrapper
        # so allow users to force the wrapper if they want
        
        if cls_spec != myself:
            obj = object.__new__(cls_spec)
            obj.__init__(component)
            return obj

        new_class = cls_spec.find_wrapper(component)
        
        obj = object.__new__(new_class)

        obj.__init__(component)

        return obj

    def __init__(self, component):
        """
        Initialize the component
        """
        if component:
            
            self.component = component
        else:
            raise RuntimeError('NULL pointer was used to initialize BaseWrapper')
    
    @abstractmethod
    def setValue(self, value: Union[bool, str, int, float]):
        'Standard base class set value method (may not currently work on all components).'
        raise NotImplementedError

    @abstractmethod
    def getValue(self) -> Union[bool, str, int, float]:
        'Standard base class get value method (may not currently work on all components).'
        raise NotImplementedError
    
    @abstractmethod
    def setFocus(self):
        '''Standard base class set focus method (may not currently work on all components).\n
        Brings the components root parent window to the top most level (z-index) and sets component as "active".'''
        raise NotImplementedError

    @abstractmethod
    def invoke(self):
        '''Standard base class invoke method (may not currently work on all components).\n
        Invoke will select / click the component without actual mouse movement
        (therefore this may work on components that are not visible).'''
        raise NotImplementedError

    @abstractmethod
    def click(self):
        '''Standard base class click method\n
        Manually performs a mouse movement and clicks the component at it's mid-point.'''
        raise NotImplementedError

    @abstractmethod
    def right_click(self):
        '''Standard base class right click method\n
        Manually performs a mouse movement and right clicks the component at it's mid-point.'''
        raise NotImplementedError
    
    @abstractmethod
    def isTopLevel(self) -> bool:
        '''Standard base class is on top method\n
        Compares the components position against the top most level (z-index) component at this position.'''
        raise NotImplementedError

    @abstractmethod
    def isVisible(self) -> bool:
        '''Standard base class is visible method\n
        Uses a OS dependant accessibility API checks.'''
        raise NotImplementedError

    @abstractmethod
    def exists(self) -> bool:
        '''Standard base class exists method\n
        Uses a OS dependant accessibility API checks.'''
        raise NotImplementedError
    
    @abstractmethod
    def getMidpoint(self) -> tuple[int, int]:
        '''Standard base class get mid point method\n
        Finds the components mid-point.\n
        Returns: 
                    x: x-position in pixels of type int
                    y: y-position in pixels of type int'''
        raise NotImplementedError
    
    @abstractmethod
    def getCoordinates(self) -> tuple[int, int, int, int]:
        '''Standard base class get coordinates method\n
        Gets the components rectangular edge positions.\n
        Returns: 
                    left: x-position of left top corner in pixels of type int
                    top: y-position of left top corner in pixels of type int
                    right: x-position of bottom right corner in pixels of type int
                    bottom: y-position of bottom right corner in pixels of type int'''
        raise NotImplementedError
    
    @abstractmethod
    def getSizes(self):
        '''Standard base class get sizes method\n
        Gets the components width and height.\n
        Returns: 
                    width: width in pixels of type int
                    height: height in pixels of type int'''
        raise NotImplementedError

    @abstractmethod
    def getChildren(self) -> UIBaseComponentWrapper:
        '''Standard base class get children method\n
        Gets all of the components children (non recursive).\n
        Returns: 
                    children: all children in a list of type UIBaseComponentWrapper
                    (type should dynamicly wrap to it's cross compatible wrapper)'''
        raise NotImplementedError
    
    @abstractmethod
    def getDescendants(self) -> UIBaseComponentWrapper:
        '''Standard base class get descendants method\n
        Gets all of the components descendants (recursive).\n
        Returns: 
                    descendants: all descendants in a list of type UIBaseComponentWrapper
                    (type should dynamicly wrap to it's cross compatible wrapper)'''
        raise NotImplementedError

    @abstractmethod
    def findAll(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> list[UIBaseComponentWrapper]:
        '''Standard base class find all method\n
        Gets all of the components children with the specified criteria.
        Raises an exception if the criteria matches no components (pre order traversal, non recursive).\n
        Args:
                    control_type: the specified control type wrapper to search (of type UIBaseComponentWrapper)
                    
                    (optional criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    components: components dynamicly wrapped to it's cross compatible custom wrapper in a list of type UIBaseComponentWrapper'''
        raise NotImplementedError
    
    @abstractmethod
    def findFirst(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> UIBaseComponentWrapper:
        '''Standard base class find first method\n
        Gets the first child component with the specified criteria.
        Raises an exception if the criteria matches no components (pre order traversal, non recursive).\n
        Args:
                    control_type: the specified control type wrapper to search (of type UIBaseComponentWrapper)
                    
                    (optional criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    component: component dynamicly wrapped to it's cross compatible custom wrapper of type UIBaseComponentWrapper'''
        raise NotImplementedError
    
    @abstractmethod
    def findAllR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> list[UIBaseComponentWrapper]:
        '''Standard base class find all recursive method\n
        Gets all of the components children with the specified criteria.
        Raises an exception if the criteria matches no components (pre order traversal, recursive).\n
        Args:
                    control_type: the specified control type wrapper to search (of type UIBaseComponentWrapper)
                    
                    (optional criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    components: components dynamicly wrapped to it's cross compatible custom wrapper in a list of type UIBaseComponentWrapper'''
        raise NotImplementedError
    
    @abstractmethod
    def findFirstR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> UIBaseComponentWrapper:
        '''Standard base class find first recursive method\n
        Gets the first child component with the specified criteria.
        Raises an exception if the criteria matches no components (pre order traversal, recursive).\n
        Args:
                    control_type: the specified control type wrapper to search (of type UIBaseComponentWrapper)
                    
                    (optional criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    component: component dynamicly wrapped to it's cross compatible custom wrapper of type UIBaseComponentWrapper'''
        raise NotImplementedError
    
    @abstractmethod
    def find(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> UIBaseComponentWrapper:
        '''Standard base class find method\n
        Finds a child component with the specified criteria.
        Raises an exception if the criteria matches > 1 or no components (non recursive).\n
        Args:
                    control_type: the specified control type wrapper to search (of type UIBaseComponentWrapper)
                    
                    (optional criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    component: component dynamicly wrapped to it's cross compatible custom wrapper of type UIBaseComponentWrapper'''
        raise NotImplementedError

    @abstractmethod
    def findR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria) -> UIBaseComponentWrapper:
        '''Standard base class find recursive method\n
        Finds a child component with the specified criteria.
        Raises an exception if the criteria matches > 1 or no components (recursive).\n
        Args:
                    control_type: the specified control type wrapper to search (of type UIBaseComponentWrapper)
                    
                    (optional criteria)
                    title: the name of the component (of type string)

                    (extra OS specific accessibility API criteria)
        Returns: 
                    component: component dynamicly wrapped to it's cross compatible custom wrapper of type UIBaseComponentWrapper'''
        raise NotImplementedError
    
    @classmethod
    @property
    @abstractmethod
    def native_control_type(cls) -> str:
        'Standard base class control type property (name of the components native control type).'
        raise NotImplementedError
    
    @classmethod
    @property
    @abstractmethod
    def control_type(cls) -> Type:
        'Standard base class control type property (name of the components control type).'
        raise NotImplementedError
    
    @property
    @abstractmethod
    def title(self) -> str:
        'Standard base class title property (name of the component).'
        raise NotImplementedError

    # _protected methods

    def _check_element_exists(self, component) -> bool:
        return not(component is None)

    def _check_elements_exist(self, components) -> bool:
        return len(components) > 0
    
    # def _wrapper_function_from_native(self, component, native_control_type: str) -> UIBaseComponentWrapper:
    #     '''Wrap objects using their native component type
    #     '''
    #     return wrapper_mapping[native_control_type](component)
    
    # def _wrapper_function(self, component, control_type: Type) -> UIBaseComponentWrapper:
    #     '''Wrap objects using the pyUIauto control types\n
    #     ( also checks if the elements aren't null )
    #     '''
    #     return control_type(component) if self._check_element_exists(component) else None
    
    # def _list_wrapper_function(self, components, control_type: Type) -> list[UIBaseComponentWrapper]:
    #     '''Wrap objects using the pyUIauto control types\n
    #     ( also checks if the elements aren't null )
    #     '''
    #     return list(control_type(component) for component in components) if self._check_elements_exist(components) else None

    def __str__(self) -> str:
        return self.control_type

class UIButtonWrapper():
    @abstractmethod
    def press(self):
        '''Button press method\n
        Similar to the invoke method, performs a button press without actual mouse movement.
        (therefore this may work on components that are not visible).'''
    
    def toggle(self, value):
        '''Button toggle method\n
        Performs a button press if the provided value != current value.
        (overrides the setValue method)'''
        return self.press() if self.getValue() != value else None

    def setValue(self, value):
        return self.toggle(value)

class UICheckBoxWrapper(): ...

class UIRadioButtonWrapper(): ...

class UITextWrapper(): ...

class UISliderWrapper(): ...

class UIEditWrapper(): ...

class UIMenuWrapper(): ...
class UIMenuItemWrapper():
    @abstractmethod
    def select(self):
        '''Menu item select method\n
        Similar to the invoke method, selects a menu item without actual mouse movement.'''
    
    def invoke(self):
        return self.select()

    def toggle(self, value) -> bool:
        '''Menu item toggle method\n
        Selects a menu item if the provided value != current value.
        (overrides the setValue method)'''
        if self.getValue() != value:
            self.select()
            return True
        else:
            return False
    
    def setValue(self, value):
        return self.toggle(value)

class UIWindowWrapper():
    @abstractmethod
    def moveResize(self, x: int = None, y: int = None, width: int = None, height: int = None):
        '''Window move resize method\n
        Moves a windows top left corner to the specified pixel points x, y (if provided)
        and resizes the window to the specified pixel width, height (if provided)
        Args:
                    (optional | default = None)
                    x: top left corner x-axis in pixels (of type int)
                    y: top left corner y axis in pixels (of type int)
                    width: width of the window size in pixels (of type int)
                    height: height of the window size in pixels (of type int)'''

    @abstractmethod
    def close(self):
        '''Window close method to press the close button\n
        Similar to a button invoke method, selects the window's close button without actual mouse movement.'''

class UIGroupWrapper(): ...
class UIStaticTextWrapper(): ...

class UIMenuBarWrapper(): ...

class UIProgressBarWrapper(): ...

class UITitleBarWrapper(): ...

# !!! Mac Specific Components !!!
class UIMenuBarItemWrapper(): ...
class UIPopUpButton(): ...

# wrapper_mapping = {wrapper.native_control_type: wrapper for wrapper in (UIButtonWrapper, UIRadioButtonWrapper, UIMenuWrapper, UIMenuItemWrapper, UIProgressBarWrapper, UITextWrapper, UISliderWrapper, UIEditWrapper, UITitleBarWrapper, UIMenuBarWrapper, UIMenuBarItemWrapper, UIWindowWrapper, UIGroupWrapper, UIStaticTextWrapper)}
