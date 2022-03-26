# mywificonnection.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

#     Now it works in STATION mode, maybe by configuration it can changed to AP mode, e.g. first time/on admin setup

import network
import time

class myWifiConnection:

    def __init__(self, configuration):
        self.config = configuration
        self.connect()
        print("myWifi init...", self.get_address())

    def get_address(self):
        if hasattr(self,'connection'):
            return self.connection.ifconfig()[0]
        return ''

    def isconnected(self):
        if hasattr(self,'connection'):
            return self.connection.isconnected()
        return False

    def connect(self, waitforcompletition = False, timeout = 5 ):
        self.connection = network.WLAN(network.STA_IF)
        if not self.connection.active(): self.connection.active(True)
        if not self.connection.isconnected():
            self.connection.connect(self.config.get_ssid(), self.config.get_passphrase())
        
        starttime = time.time()
        lasttime = time.time()
        while timeout<(lasttime-starttime) and not self.connection.isconnected():
            lasttime = time.time()
            
        return self.connection.isconnected()
        
