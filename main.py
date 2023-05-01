import time

from pyuiauto.application import UIApplication
from pyuiauto.components import UIMenuItem

with UIApplication("EVO", "C:\\Program Files\\Audient\\EVO\\EVO.exe") as app:

    with app.getSystemTrayIcon() as icon:
        icon.right_click()
        popup = app.window(title="EVO")
        popup.findFirstR(title="Show Mixer", control_type=UIMenuItem).click()
    
    main = app.window(title="EVO Mixer")
    main.findFirstR(title="View", control_type=UIMenuItem).click()
    popup = app.window(title="EVO")
    micpre = popup.findFirstR(title='Show Mic Pre Controls', control_type=UIMenuItem)
    if not micpre.getValue():
        micpre.click()

    print(f"Mic Pre Controls: {micpre.getValue()}")
        
    time.sleep(3)
