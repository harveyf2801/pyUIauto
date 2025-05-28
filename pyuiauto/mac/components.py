#___MODULES___
from __future__ import annotations
from typing import Type
import time
from abc import ABCMeta
import logging

# pip installed modules
try:
    from atomacos import NativeUIElement
except ImportError: # requires pip install
    raise ModuleNotFoundError('To install the required modules use pip install atomacos (MacOS ONLY)')


from ApplicationServices import AXValueCreate, kAXValueCGPointType, kAXValueCGSizeType
import Quartz.CoreGraphics as CG

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
        try:
            control_type = component.AXRole
        except:
            control_type = "No Role"
            logging.warning(f"Component: {component} | has no control type / AXRole attribute")

        if control_type in UIBaseComponentWrapperMeta.control_type_to_cls:
            wrapper_match = UIBaseComponentWrapperMeta.control_type_to_cls[control_type]
        else:
            raise NotImplementedError(f"{component} doesn't have an implemented wrapper")

        return wrapper_match

#___DEFINING_NATIVE_METHODS___

class UIBaseComponent(UIBaseComponentWrapper, metaclass=UIBaseComponentMeta):

    def __new__(cls, component: NativeUIElement):
        """Construct the control wrapper"""
        return super(UIBaseComponent, cls)._create_wrapper(cls, component, UIBaseComponent)

    # -----------------------------------------------------------
    def __init__(self, component: NativeUIElement):
        UIBaseComponentWrapper.__init__(self, component)

        self.component: NativeUIElement

    def getValue(self):
        return self.component.AXValue
    
    def setValue(self, value):
        self.component.setString("AXValue", value)
        # self.component.AXValue = value
    
    def setFocus(self):
        self.component.activate()
    
    def invoke(self):
        self.component.Press()

    def click(self):
        self.component.clickMouseButtonLeft(self.getMidpoint())
    
    def right_click(self):
        self.component.clickMouseButtonRight(self.getMidpoint())

    def isTopLevel(self):
        x, y, _, _= self.getCoordinates()
        is_visible = self.component.getApplication().getElementAtPosition((x, y)) == self.component
        return is_visible

    def isVisible(self):
        x, y, _, _= self.getCoordinates()
        is_visible = self.component.getApplication().getElementAtPosition((x, y)) == self.component
        return is_visible

    def exists(self):
        return hasattr(self.component, "AXRole")
    
    def getMidpoint(self):
        return ((self.component.AXPosition[0] + self.component.AXSize[0] / 2), (self.component.AXPosition[1] + self.component.AXSize[1] / 2))

    def getCoordinates(self):
        x, y = self.component.AXPosition
        w, h = self.component.AXSize
        return x, y, x+w, y+h
    
    def getSizes(self):
        return self.component.AXSize
    
    def getChildren(self):
        return list(UIBaseComponent(component) for component in self.component.AXChildren)
    
    getDescendants = getChildren
    
    def _wait_find(self, function, check_function, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        for i in (  {"conversion": "title", "apple": "AXTitle"},
                    {"conversion": "description", "apple": "AXDescription"},
                ):
            try:
                criteria[i["apple"]] = criteria.pop(i["conversion"])
            except KeyError:
                pass

        timeafter = time.time() + timeout
        while time.time() < timeafter:
            item = function(AXRole=control_type.native_control_type, **criteria)
            item_check = check_function(item)
            if item_check:
                if type(item) == list:
                    return list(UIBaseComponent(i) for i in item)
                else:
                    return UIBaseComponent(item)
            time.sleep(retry_interval)
        raise ElementNotFound(f"Element - ControlType: {control_type.native_control_type} - {criteria} - not found after {timeout} seconds")

    def findFirst(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self._wait_find(function=self.component.findFirst,
                                check_function=self._check_element_exists,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findAll(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self._wait_find(function=self.component.findAll,
                                check_function=self._check_elements_exist,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findFirstR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self._wait_find(function=self.component.findFirstR,
                                check_function=self._check_element_exists,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findAllR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        return self._wait_find(function=self.component.findAllR,
                                check_function=self._check_elements_exist,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)
    
    def find(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.01, **criteria):
        items = self.findAll(control_type, timeout, retry_interval, **criteria)
        
        if len(items) > 1:
            raise ElementNotFound(f"{len(items)} Elements found matching the criteria - ControlType: {control_type} - {criteria}")

        return items[0]
    
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
    def title(self) -> str:
        return self.component.AXTitle


# ============================================


class UIAppRoot(UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXApplication"


# ============================================


class UIButton(UIButtonWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXButton"
    
    def press(self):
        self.invoke()
    
    def setValue(self, value):
        return super().setValue(value)

class UICheckBox(UICheckBoxWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXCheckBox"
    
class UIRadioButton(UIRadioButtonWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXRadioButton"

class UIText(UITextWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXText"

class UISlider(UISliderWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXSlider"

class UIEdit(UIEditWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXTextArea"

class UIMenu(UIMenuWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXMenu"

class UIMenuItem(UIMenuItemWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXMenuItem"

    def getValue(self) -> bool:
        return self.component.AXMenuItemMarkChar != None

    def select(self):
        self.component.Press()
    
    def setValue(self, value):
        return super().setValue(value)

class UIWindow(UIWindowWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXWindow"

    def moveResize(self, x=None, y=None, width=None, height=None):
        left, top, _, _ = self.getCoordinates()
        w, h = self.getSizes()

        # if no X is specified - so use current coordinate
        if x is None:
            x = left

        # if no Y is specified - so use current coordinate
        if y is None:
            y = top

        # if no width is specified - so use current width
        if width is None:
            width = w

        # if no height is specified - so use current height
        if height is None:
            height = h

        # ask for the window to be moved
        point = CG.CGPoint(x=x, y=y)
        self.component.AXPosition = AXValueCreate(kAXValueCGPointType, point)

        # ask for the window to be resized
        size = CG.CGSize(width=width, height=height)
        self.component.AXSize = AXValueCreate(kAXValueCGSizeType, size)

    def close(self):
        self.component.AXCloseButton.Press()

class UIGroup(UIGroupWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXGroup"

class UIStaticText(UIStaticTextWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXStaticText"

class UITitleBar(UITitleBarWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXTitleBar"

class UIMenuBar(UIMenuBarWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXMenuBar"

class UIProgressBar(UIProgressBarWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXProgressIndicator"

# !!! Mac Specific !!!

class UIMenuBarItem(UIMenuItemWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXMenuBarItem"

class UIPopUpButton(UIButtonWrapper, UIBaseComponent):
    @classmethod
    @property
    def native_control_type(cls) -> str:
        return "AXPopUpButton"