import time

from pyuiauto.application import UIApplication

app = UIApplication("EVO", "C:\\Program Files\\Audient\\EVO\\EVO.exe")

app.launchApp()
app.connectApp()

with app.getSystemTrayIcon() as icon:
    icon.right_click()
    
time.sleep(3)

app.terminateApp()