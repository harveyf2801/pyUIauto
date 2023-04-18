#___MODULES___
from __future__ import annotations
from typing import Type
import time
from abc import ABCMeta

from ApplicationServices import AXValueCreate, kAXValueCGPointType, kAXValueCGSizeType
import Quartz.CoreGraphics as CG

#___MY_MODULES___
from pyuiauto.src.exceptions import ElementNotFound
from pyuiauto.src.base.components import *


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

        if component.AXRole in UIBaseComponentWrapperMeta.control_type_to_cls:
            wrapper_match = UIBaseComponentWrapperMeta.control_type_to_cls[component.AXRole]
        else:
            raise NotImplementedError(f"{component} doesn't have an implemented wrapper")

        return wrapper_match

#___DEFINING_NATIVE_METHODS___

class UIBaseComponent(UIBaseComponentWrapper, metaclass=UIBaseComponentMeta):

    def __new__(cls, component):
        """Construct the control wrapper"""
        return super(UIBaseComponent, cls)._create_wrapper(cls, component, UIBaseComponent)

    # -----------------------------------------------------------
    def __init__(self, component):
        UIBaseComponentWrapper.__init__(self, component)

    def getValue(self):
        return self.component.AXValue
    
    def setValue(self, value):
        self.component.setString("AXValue", value)
    
    def setFocus(self):
        self.component.activate()
    
    def invoke(self):
        self.component.Press()

    def click(self):
        self.component.clickMouseButtonLeft(self.getMidpoint())
    
    def right_click(self):
        self.component.clickMouseButtonRight(self.getMidpoint())
    
    def isVisible(self):
        x, y, _, _= self.getCoordinates()
        is_visible = self.component.getApplication().getElementAtPosition((x, y)) == self.component
        return is_visible
    
    def getMidpoint(self):
        return ((self.component.AXPosition[0] + self.component.AXSize[0] / 2), (self.component.AXPosition[1] + self.component.AXSize[1] / 2))

    def getCoordinates(self):
        x, y = self.component.AXPosition
        w, h = self.component.AXSize
        return x, y, x+w, y+h
    
    def getSizes(self):
        return self.component.AXSize
    
    def getChildren(self):
        return list(self._wrapper_function_from_native(component, component.AXRole) for component in self.component.AXChildren)
    
    getDescendants = getChildren
    
    def _wait_find(self, function, check_function, control_type: Type, timeout: int = 1, retry_interval: float = 0.1, **criteria):
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

    def findFirst(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findFirst,
                                check_function=self._check_element_exists,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findAll(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findAll,
                                check_function=self._check_elements_exist,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findFirstR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findFirstR,
                                check_function=self._check_element_exists,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findAllR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findAllR,
                                check_function=self._check_elements_exist,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)
    
    def find(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        items = self.findAll(control_type, timeout, retry_interval, **criteria)
        
        if len(items) > 1:
            raise ElementNotFound(f"{len(items)} Elements found matching the criteria - ControlType: {control_type} - {criteria}")

        return items[0]
    
    def findR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        items = self.findAllR(control_type, timeout, retry_interval, **criteria)
        
        if len(items) > 1:
            raise ElementNotFound(f"{len(items)} Elements found matching the criteria - ControlType: {control_type} - {criteria}")

        return items[0]
    
    @property
    def title(self):
        return self.component.AXTitle
    
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
    

class UIButton(UIBaseComponent, UIButtonWrapper):
    native_control_type: str = "AXButton"
    
    def press(self):
        self.invoke()

class UIApplication(UIBaseComponent):
    native_control_type: str = "AXApplication"

class UIWindow(UIBaseComponent, UIWindowWrapper):
    native_control_type: str = "AXWindow"

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




# ============================================





class UIButton(UIBaseComponent, UIButtonWrapper):
    native_control_type: str = "AXButton"
    
    def press(self):
        self.invoke()

class UIRadioButton(UIBaseComponent, UIRadioButtonWrapper):
    native_control_type: str = "AXRadioButton"

class UIText(UIBaseComponent, UITextWrapper):
    native_control_type: str = "AXText"

class UISlider(UIBaseComponent, UISliderWrapper):
    native_control_type: str = "AXSlider"

class UIEdit(UIBaseComponent, UIEditWrapper):
    native_control_type: str = "AXTextArea"

class UIMenu(UIBaseComponent, UIMenuWrapper):
    native_control_type: str = "AXMenu"

class UIMenuItem(UIBaseComponent, UIMenuItemWrapper):
    native_control_type: str = "AXMenuItem"

    def select(self):
        self.invoke()

class UIWindow(UIBaseComponent, UIWindowWrapper):
    native_control_type: str = "AXWindow"

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

class UIGroup(UIBaseComponent, UIGroupWrapper):
    name="AXGroup"

class UIStaticText(UIBaseComponent, UIStaticTextWrapper):
    name="AXStaticText"

class UITitleBar(UIBaseComponent, UITitleBarWrapper):
    name="AXTitleBar"

class UIMenuBar(UIBaseComponent, UIMenuBarWrapper):
    native_control_type: str = "AXMenuBar"

class UIProgressBar(UIBaseComponent):
    native_control_type: str = "AXProgressIndicator"

# !!! Mac Specific !!!

class UIMenuBarItem(UIBaseComponent, UIMenuItemWrapper):
    native_control_type: str = "AXMenuBarItem"