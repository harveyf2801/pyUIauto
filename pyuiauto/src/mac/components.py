#___MY_MODULES___
from pyuiauto.src.exceptions import ElementNotFound
from pyuiauto.src.components import UIBaseComponentWrapper, UIButtonWrapper

#___MODULES___
from typing import Type
import time

# from ApplicationServices import AXValueCreate, kAXValueCGPointType, kAXValueCGSizeType
# import Quartz.CoreGraphics as CG

#___DEFINING_NATIVE_METHODS___
class UIBaseComponent(UIBaseComponentWrapper):
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
            item = function(AXRole=control_type.name, **criteria)
            item_check = check_function(item, control_type)
            if item_check:
                return item_check
            time.sleep(retry_interval)
        raise ElementNotFound(f"Element - ControlType: {control_type.name} - {criteria} - not found after {timeout} seconds")

    def findFirst(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findFirst,
                                check_function=self._wrapper_function,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findAll(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findAll,
                                check_function=self._list_wrapper_function,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findFirstR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findFirstR,
                                check_function=self._wrapper_function,
                                control_type=control_type,
                                timeout=timeout,
                                retry_interval = retry_interval,
                                **criteria)

    def findAllR(self, control_type: Type, timeout: int = 1, retry_interval: float = 0.5, **criteria):
        return self._wait_find(function=self.component.findAllR,
                                check_function=self._list_wrapper_function,
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
        raise NotImplementedError
    
    @classmethod
    @property
    def control_type(cls) -> Type:
        return type(cls)
    
    @property
    def title(self) -> str:
        return self.component.AXTitle
    

class UIButton(UIBaseComponent, UIButtonWrapper):
    name = "AXButton"
    
    def press(self):
        self.invoke()