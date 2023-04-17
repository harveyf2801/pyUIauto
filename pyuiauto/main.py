from abc import ABC, abstractmethod
from platform import system

# import scipy.io as sio
# import os, sys
# import argparse

# class FrameworkCreator(ABC):
#     @staticmethod
#     def build_framework() -> Framework:
#         if system() == "Darwin":
#             # pip installed modules
#             try:
#                     import atomacos
#             except ImportError: # requires pip install
#                     raise ModuleNotFoundError('To install the required modules use pip install atomacos (Mac ONLY)')
            
#             return UIApplication()
        
#         elif system() == "Windows":
#             # pip installed modules
#             try:
#                     import pywinauto
#             except ImportError: # requires pip install
#                     raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')
            
#             return UIApplication()
#         else:
#             raise OSError("The current OS isn't supported with this framework")


def main():

    from pyuiauto.src.mac.application import UIApplication
    import time

    app = UIApplication("EVO", "/Applications/EVO.app")

    app.launchApp()
    app.connectApp()
    app.windows()
    
    time.sleep(2)

    app.terminateApp()



if __name__ == '__main__':
    
    main()