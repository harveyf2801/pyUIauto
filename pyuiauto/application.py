from platform import system

if system() == "Darwin":
    from pyuiauto.mac.application import UIApplication

elif system() == "Windows":
    from pyuiauto.win.application import UIApplication

else:
    raise OSError("The current OS isn't supported with this framework")

