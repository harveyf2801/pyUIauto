from platform import system

if system() == "Darwin":
    # pip installed modules
    try:
            import atomacos
    except ImportError: # requires pip install
            raise ModuleNotFoundError('To install the required modules use pip install atomacos (Mac ONLY)')

elif system() == "Windows":
    # pip installed modules
    try:
            import pywinauto
    except ImportError: # requires pip install
            raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')
    
else:
    raise OSError("The current OS isn't supported with this framework")

from pyuiauto.src.application import UIApplication
from pyuiauto.src.components import UIButton, UIWindow, UISlider


def main():



    import time

    app = UIApplication("EVO", "/Applications/EVO.app")

    app.launchApp()
    app.connectApp()
    win = app.window(title="EVO Mixer", timeout=10)

    # win.moveResize(0, 0, 100, 100)
    pan = win.findFirstR(title="Mic 1 pan", control_type=UISlider)
    pan.setValue(0)
    
    app.terminateApp()



if __name__ == '__main__':
    
    main()