# ___MODULES___
from __future__ import annotations
from abc import ABC, ABCMeta, abstractmethod
from typing import Type, Union

# ___CLASSES___

class UIBaseComponentMeta(ABCMeta):

    """Metaclass for UIComponentWrapper objects"""
    control_type_to_cls = {}

    def __init__(cls, name, bases, attrs):
        """Register the control types"""

        super().__init__(cls, name, bases, attrs)

        for t in cls._control_types:
            UiaMeta.control_type_to_cls[t] = cls

    @staticmethod
    def find_wrapper(element):
        """Find the correct wrapper for this UIA element"""
        # Set a general wrapper by default
        wrapper_match = UIAWrapper

        # Check for a more specific wrapper in the registry
        if element.control_type in UiaMeta.control_type_to_cls:
            wrapper_match = UiaMeta.control_type_to_cls[element.control_type]

        return wrapper_match

class UIBaseComponentWrapper(object, metaclass=UIBaseComponentMeta):
    def __new__(cls, component):
        return UIBaseComponentWrapper._create_wrapper(cls, component, UIBaseComponentWrapper)
    
    @staticmethod
    def _create_wrapper(cls_spec, element_info, myself):
        """Create a wrapper object according to the specified element info"""
        # only use the meta class to find the wrapper for BaseWrapper
        # so allow users to force the wrapper if they want
        if cls_spec != myself:
            obj = object.__new__(cls_spec)
            obj.__init__(element_info)
            return obj

        new_class = cls_spec.find_wrapper(element_info)
        obj = object.__new__(new_class)

        obj.__init__(element_info)

        return obj
    
    def __init__(self, component) -> None:
        self.component = component
    
    @abstractmethod
    def setValue(self, value: Union[bool, str, int, float]):
        'Standard base class set value method (may not currently work on all components).'

    @abstractmethod
    def getValue(self) -> Union[bool, str, int, float]:
        'Standard base class get value method (may not currently work on all components).'
    
    @abstractmethod
    def setFocus(self):
        '''Standard base class set focus method (may not currently work on all components).\n
        Brings the components root parent window to the top most level (z-index) and sets component as "active".'''

    @abstractmethod
    def invoke(self):
        '''Standard base class invoke method (may not currently work on all components).\n
        Invoke will select / click the component without actual mouse movement
        (therefore this may work on components that are not visible).'''

    @abstractmethod
    def click(self):
        '''Standard base class click method\n
        Manually performs a mouse movement and clicks the component at it's mid-point.'''

    @abstractmethod
    def right_click(self):
        '''Standard base class right click method\n
        Manually performs a mouse movement and right clicks the component at it's mid-point.'''

    @abstractmethod
    def isVisible(self) -> bool:
        '''Standard base class is visible method\n
        Uses a combination of OS dependant accessibility API checks aswell as comparing the
        components position against the top most level (z-index) component at this position.'''
    
    @abstractmethod
    def getMidpoint(self) -> tuple[int, int]:
        '''Standard base class get mid point method\n
        Finds the components mid-point.\n
        Returns: 
                    x: x-position in pixels of type int
                    y: y-position in pixels of type int'''
    
    @abstractmethod
    def getCoordinates(self) -> tuple[int, int, int, int]:
        '''Standard base class get coordinates method\n
        Gets the components rectangular edge positions.\n
        Returns: 
                    left: x-position of left top corner in pixels of type int
                    top: y-position of left top corner in pixels of type int
                    right: x-position of bottom right corner in pixels of type int
                    bottom: y-position of bottom right corner in pixels of type int'''
    
    @abstractmethod
    def getSizes(self):
        '''Standard base class get sizes method\n
        Gets the components width and height.\n
        Returns: 
                    width: width in pixels of type int
                    height: height in pixels of type int'''

    @abstractmethod
    def getChildren(self) -> UIBaseComponentWrapper:
        '''Standard base class get children method\n
        Gets all of the components children (non recursive).\n
        Returns: 
                    children: all children in a list of type UIBaseComponentWrapper
                    (type should dynamicly wrap to it's cross compatible wrapper)'''
    
    @abstractmethod
    def getDescendants(self) -> UIBaseComponentWrapper:
        '''Standard base class get descendants method\n
        Gets all of the components descendants (recursive).\n
        Returns: 
                    descendants: all descendants in a list of type UIBaseComponentWrapper
                    (type should dynamicly wrap to it's cross compatible wrapper)'''

    @abstractmethod
    def findAll(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria) -> list[UIBaseComponentWrapper]:
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
    
    @abstractmethod
    def findFirst(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria) -> UIBaseComponentWrapper:
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
    
    @abstractmethod
    def findAllR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria) -> list[UIBaseComponentWrapper]:
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
    
    @abstractmethod
    def findFirstR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria) -> UIBaseComponentWrapper:
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
    
    @abstractmethod
    def find(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria) -> UIBaseComponentWrapper:
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

    @abstractmethod
    def findR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria) -> UIBaseComponentWrapper:
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
    
    @property
    @abstractmethod
    def native_control_type(self):
        'Standard base class control type property (name of the components native control type).'
    
    @property
    @abstractmethod
    def control_type(self):
        'Standard base class control type property (name of the components control type).'
    
    @property
    @abstractmethod
    def title(self):
        'Standard base class title property (name of the component).'

    # _protected methods

    def _check_element_exists(self, component):
        return not(component is None)

    def _check_elements_exist(self, components):
        return len(components) > 0
    
    def _wrapper_function_from_native(self, component, native_control_type: str):
        '''Wrap objects using their native component type
        '''
        return wrapper_mapping[native_control_type](component)
    
    def _wrapper_function(self, component, control_type: Type):
        '''Wrap objects using the pyUIauto control types\n
        ( also checks if the elements aren't null )
        '''
        return control_type(component) if self._check_element_exists(component) else None
    
    def _list_wrapper_function(self, components, control_type: Type):
        '''Wrap objects using the pyUIauto control types\n
        ( also checks if the elements aren't null )
        '''
        return list(control_type(component) for component in components) if self._check_elements_exist(components) else None

    def __str__(self) -> str:
        return self.control_type

class UIButtonWrapper(UIBaseComponentWrapper):
    @abstractmethod
    def press(self):
        '''Button press method\n
        Similar to the invoke method, performs a button press without actual mouse movement.
        (therefore this may work on components that are not visible).'''
    
    invoke = press

    def toggle(self, value):
        '''Button toggle method\n
        Performs a button press if the provided value != current value.
        (overrides the setValue method)'''
        return self.press() if self.getValue() != value else None

    setValue = toggle

class UIRadioButtonWrapper(UIBaseComponentWrapper): ...

class UITextWrapper(UIBaseComponentWrapper): ...

class UISliderWrapper(UIBaseComponentWrapper): ...

class UIEditWrapper(UIBaseComponentWrapper): ...

class UIMenuWrapper(UIBaseComponentWrapper): ...
class UIMenuItemWrapper(UIBaseComponentWrapper):
    @abstractmethod
    def select(self):
        '''Menu item select method\n
        Similar to the invoke method, selects a menu item without actual mouse movement.'''
    
    invoke = select

    def toggle(self, value) -> bool:
        '''Menu item toggle method\n
        Selects a menu item if the provided value != current value.
        (overrides the setValue method)'''
        if self.getValue() != value:
            self.select()
            return True
        else:
            return False
    
    setValue = toggle

class UIWindowWrapper(UIBaseComponentWrapper):
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

class UIGroupWrapper(UIBaseComponentWrapper): ...
class UIStaticTextWrapper(UIBaseComponentWrapper): ...

class UIMenuBarWrapper(UIBaseComponentWrapper): ...

class UIProgressBarWrapper(UIBaseComponentWrapper): ...

class UITitleBarWrapper(UIBaseComponentWrapper): ...

# !!! Mac Specific Components !!!
class UIMenuBarItemWrapper(UIBaseComponentWrapper): ...


wrapper_mapping = {wrapper.native_control_type: wrapper for wrapper in (UIButtonWrapper, UIRadioButtonWrapper, UIMenuWrapper, UIMenuItemWrapper, UIProgressBarWrapper, UITextWrapper, UISliderWrapper, UIEditWrapper, UITitleBarWrapper, UIMenuBarWrapper, UIMenuBarItemWrapper, UIWindowWrapper, UIGroupWrapper, UIStaticTextWrapper)}
