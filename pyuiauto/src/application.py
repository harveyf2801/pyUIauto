from platform import system

if system() == "Darwin":
    from pyuiauto.src.mac.application import UIApplication

elif system() == "Windows":
    from pyuiauto.src.win.application import UIApplication

else:
    raise OSError("The current OS isn't supported with this framework")