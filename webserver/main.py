# main.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

# 1, Read Configuration
from myconfiguration import myConfiguration
myconfig = myConfiguration()

# 2, Start Internet/Wifi connection
from mywificonnection import myWifiConnection
myconnection = myWifiConnection( myconfig )

# 3, Start Webserver and handle requests
from mywebserver import myWebServer
myserver = myWebServer( myconnection )

import utime
print("Current time: %04d-%02d-%02d %02d:%02d:%02d" % utime.localtime()[:6] )

myserver.start()


