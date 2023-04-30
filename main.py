import time

from pyuiauto.application import UIApplication

app = UIApplication("EVO", "C:\\Program Files\\Audient\\EVO\\EVO.exe")

app.launchApp()
app.connectApp()

for i in app.windows():
    print(i.title)
    i.setFocus()
    i.close()
    
    time.sleep(1)

app.terminateApp()