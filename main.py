import logging
from colorama import init, Fore, Style
from platform import system as get_os
from os.path import expanduser
from sys import exit
from pyuiauto.application import UIApplication
from pyuiauto.components import UIButton, UIGroup, UIPopUpButton


# LOGGING SETUP
init(autoreset=True)

logging.basicConfig(
  level=logging.DEBUG,
  format=f'{Style.DIM}%(asctime)s\t[%(levelname)s]\t%(filename)s:%(lineno)d{Style.RESET_ALL}\t%(message)s'
)
logger = logging.getLogger("ORIA-RoomControl")


# HELPER FUNCTIONS
def get_app_path() -> str:
    return {
        "Darwin": "/Applications/ORIA.app",
        "Windows": expanduser("~\\AppData\\Local\\Programs\\Audient\\ORIA.exe")
    }.get(get_os(), None)

def launch_app() -> UIApplication:
    app_path = get_app_path()
    if app_path is None:
        raise NotImplementedError(f"Unsupported OS: {get_os()}")
    app = UIApplication(appName="ORIA", appPath=app_path)
    app.launchApp()
    app.connectApp()
    return app


# MAIN
def main():
    app = launch_app()
    logger.info(f"{Fore.GREEN}Connected to ORIA app: {app.appName} at {app.appPath}{Style.RESET_ALL}")
    main_window = app.window(title="ORIA", timeout=2)

    monitoring_panel = main_window.findR (control_type=UIGroup, title="Monitoring")
    input_source = monitoring_panel.findR (control_type=UIPopUpButton, title="Input Source")
    input_source.click()

    with app.getPopupMenu("menu") as popup:
      popup.getMenuItemFromPath("DANTE")
    
    import time
    time.sleep(2)

    main_window.close()
    app.terminateApp()


if __name__ == "__main__":
    main()
    