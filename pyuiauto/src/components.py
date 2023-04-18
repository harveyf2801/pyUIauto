from platform import system

if system() == "Darwin":
    from pyuiauto.src.mac.components import UIButton, UIEdit, UIMenu, UIGroup, UIMenuBar, UIMenuBarItem, UIMenuItem, UISlider, UIProgressBar, UIRadioButton, UIWindow, UIText, UIStaticText, UITitleBar

elif system() == "Windows":
    from pyuiauto.src.win.components import UIButton, UIEdit, UIMenu, UIGroup, UIMenuBar, UIMenuBarItem, UIMenuItem, UISlider, UIProgressBar, UIRadioButton, UIWindow, UIText, UIStaticText, UITitleBar