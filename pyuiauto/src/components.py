from platform import system

if system() == "Darwin":
    from pyuiauto.src.mac.components import UIButton, UIWindow

elif system() == "Windows":
    from pyuiauto.src.win.components import UIButton, UIWindow