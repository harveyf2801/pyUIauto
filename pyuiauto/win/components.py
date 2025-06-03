#___MODULES___
from __future__ import annotations
from typing import Type
import time
from abc import ABCMeta
import logging

# pip installed modules
try:
        from pywinauto.controls.uiawrapper import UIAWrapper
        from pywinauto.keyboard import send_keys
        from pywinauto.timings import wait_until
        from pywinauto.uia_defines import NoPatternInterfaceError
except ImportError: # requires pip install
        raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')


#___MY_MODULES___
from pyuiauto.exceptions import ElementNotFound
from pyuiauto.base.components import *


#___DEFINING_NATIVE_WRAPPER_META___

class UIBaseComponentMeta(UIBaseComponentWrapperMeta):
    """Metaclass for UIComponent objects"""

    control_type_to_cls = {}

    def __init__(cls, name, bases, attrs):
        """Register the control types"""

        UIBaseComponentWrapperMeta.__init__(cls, name, bases, attrs)

        if name != "UIBaseComponent":
            UIBaseComponentMeta.control_type_to_cls[cls.native_control_type] = cls

    @staticmethod
    def find_wrapper(component):
        """Find the correct wrapper for this UIA component"""
        # Set a general wrapper by default
        wrapper_match = UIBaseComponent

        # Check for a more specific wrapper in the registry
        control_type = component.element_info.control_type

        if control_type in UIBaseComponentWrapperMeta.control_type_to_cls:
            wrapper_match = UIBaseComponentWrapperMeta.control_type_to_cls[control_type]
        else:
            raise NotImplementedError(f"{component} doesn't have an implemented wrapper")

        return wrapper_match






#___DEFINING_NATIVE_METHODS___

class UIBaseComponent(UIBaseComponentWrapper, metaclass=UIBaseComponentMeta):

    def __new__(cls, component: UIAWrapper):
        """Construct the control wrapper"""
        return super(UIBaseComponent, cls)._create_wrapper(cls, component, UIBaseComponent)

    # -----------------------------------------------------------
    def __init__(self, component: UIAWrapper):
        UIBaseComponentWrapper.__init__(self, component)

    def getValue(self):
        return self.component.iface_value
    
    def setValue(self, value):
        self.component.set_value(value)
    
    def setFocus(self):
        self.component.set_focus()
    
    def invoke(self):
        self.component.invoke()

    def click(self):
        self.component.click_input()
    
    def right_click(self):
        self.component.right_click_input()
    
    def isTopLevel(self):
        x, y, _, _= self.getCoordinates()
        return self.component.from_point(x, y).element_info.name == self.component.element_info.name

    def isVisible(self):
        return self.component.is_visible()
    
    def exists(self):
        raise self.isVisible()
    
    def getMidpoint(self):
        return self.component.rectangle().mid_point()
    
    def getCoordinates(self):
        rectangle = self.component.rectangle()
        return rectangle.left, rectangle.top, rectangle.right, rectangle.bottom
    
    def getSizes(self):
        rectangle = self.component.rectangle()
        return rectangle.width(), rectangle.height()
    
    def getChildren(self):
        return list(UIBaseComponent(component) for component in self.component.children())

    def getDescendants(self):
        return list(UIBaseComponent(component) for component in self.component.descendants())
    
    def _wait_find(self, function, check_function, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        timeafter = time.time() + timeout
        while time.time() < timeafter:
            item = function(control_type=control_type.native_control_type, **criteria)
            item_check = check_function(item)
            if item_check:
                if type(item) == list:
                    return list(UIBaseComponent(i) for i in item)
                else:
                    return UIBaseComponent(item)
            time.sleep(retry_interval)
        raise ElementNotFound(f"CheckFunction returned: Element - ControlType: {control_type.native_control_type} - {criteria} - not found after {timeout} seconds")
        
    def findAll(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self._wait_find(function=self.component.children,
                        check_function=self._check_elements_exist,
                        control_type=control_type,
                        timeout=timeout,
                        retry_interval=retry_interval,
                        **criteria)
    
    def findFirst(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self.findAll(control_type, timeout, retry_interval, **criteria)[0]

    def find(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        items = self.findAll(control_type, timeout, retry_interval, **criteria)
        
        if len(items) > 1:
            raise ElementNotFound(f"{len(items)} Elements found matching the criteria - ControlType: {control_type} - {criteria}")

        return items[0]
    
    def findAllR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self._wait_find(function=self.component.descendants,
                        check_function=self._check_elements_exist,
                        control_type=control_type,
                        timeout=timeout,
                        retry_interval=retry_interval,
                        **criteria)
    
    def findFirstR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self.findAllR(control_type, timeout, retry_interval, **criteria)[0]

    def findR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        items = self.findAllR(control_type, timeout, retry_interval, **criteria)
        
        if len(items) > 1:
            raise ElementNotFound(f"{len(items)} Elements found matching the criteria - ControlType: {control_type} - {criteria}")

        return items[0]
    
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return None
    
    @classmethod
    @property
    def control_type(cls) -> Type:
        return type(cls)
    
    @property
    def title(self):
        return self.component.element_info.name
    
    

class UIButton(UIButtonWrapper, UIBaseComponent):
    native_control_type: str = "Button"

    def getValue(self):
        return self.component.get_toggle_state()
    
    def press(self):
        self.component.click()
    
    def setValue(self, value):
        return super().setValue(value)

class UICheckBox(UICheckBoxWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "CheckBox"
    
class UIRadioButton(UIRadioButtonWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "RadioButton"
    
    def getValue(self):
        return self.component.get_toggle_state()

class UIText(UITextWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "Text"
    
class UISlider(UISliderWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "Slider"

    def getValue(self):
        return self.component.value()

class UIEdit(UIEditWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "Edit"

    def getValue(self):
        return self.component.get_value()
    
    def setValue(self, value):
        self.component.set_focus()
        self.component.invoke()
        send_keys(str(value) + "{ENTER}")

class UIMenu(UIMenuWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "Menu"
    
class UIMenuItem(UIMenuItemWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "MenuItem"

    def getValue(self):
        try:
            return bool(self.component.iface_toggle)
        except NoPatternInterfaceError:
            return False

    def select(self):
        self.component.select()
    
    def setValue(self, value):
        return super().setValue(value)

class UIWindow(UIWindowWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "Window"
    
    def moveResize(self, x=None, y=None, width=None, height=None):
        cur_rect = self.component.rectangle()

        # if no X is specified - so use current coordinate
        if x is None:
            x = cur_rect.left

        # if no Y is specified - so use current coordinate
        if y is None:
            y = cur_rect.top

        # if no width is specified - so use current width
        if width is None:
            width = cur_rect.width()

        # if no height is specified - so use current height
        if height is None:
            height = cur_rect.height()

        # ask for the window to be moved
        self.component.iface_transform.Move(x, y)
        self.component.iface_transform.Resize(width, height)

    def close(self):
        self.component.close()

class UIGroup(UIGroupWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "Custom"

class UIStaticText(UIStaticTextWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "Text"

    def getValue(self):
        return self.component.window_text()

class UITitleBar(UITitleBarWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "TitleBar"
        
class UIMenuBar(UIMenuBarWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "MenuBar"

class UIProgressBar(UIProgressBarWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "ProgressBar"

    def getValue(self) -> float:
        return float(self.component.legacy_properties()['Value'])

# !!! Mac Specific !!!

class UIMenuBarItem(UIMenuItem, UIBaseComponent): ...
class UIPopUpButton(UIButton, UIBaseComponent): ...