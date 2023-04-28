from platform import system

def test_os_compatibility():

    if not (system() in ["Darwin", "Windows"]):
        raise OSError("The current OS isn't supported with this framework")

def test_python_modules():

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