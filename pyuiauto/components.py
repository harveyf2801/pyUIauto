from platform import system

if system() == "Darwin":
    from pyuiauto.mac.components import UIButton, UIEdit, UIMenu, UIGroup, UIMenuBar, UIMenuBarItem, UIMenuItem, UISlider, UIProgressBar, UIRadioButton, UIWindow, UIText, UIStaticText, UITitleBar

elif system() == "Windows":
    from pyuiauto.win.components import UIButton, UIEdit, UIMenu, UIGroup, UIMenuBar, UIMenuBarItem, UIMenuItem, UISlider, UIProgressBar, UIRadioButton, UIWindow, UIText, UIStaticText, UITitleBar