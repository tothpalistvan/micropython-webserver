# mywificonnection.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

import network
import time

class myWifiConnection:

    def __init__(self, configuration):
        self.config = configuration
        self.wifimode = self.config.getWifiMode()
        self.port = self.config.get_port()
        self.connect()
        print("myWifi init...", self.get_address())

    def get_address(self):
        if hasattr(self,'connection'):
            return self.connection.ifconfig()[0]
        return ''

    def get_port(self):
        return self.port

    def isconnected(self):
        if hasattr(self,'connection'):
            return self.connection.isconnected()
        return False

    def connect(self, waitforcompletition = False, timeout = 5 ):
        
        if self.wifimode == "station":
            self.connection = network.WLAN(network.STA_IF)
            if not self.connection.active(): self.connection.active(True)
            if not self.connection.isconnected():
                self.connection.connect(self.config.get_ssid(), self.config.get_passphrase())
        else: # AP mode
            self.connection = network.WLAN(network.AP_IF)
            self.connection.config(essid=self.config.get_ssid(), authmode=network.AUTH_WPA_WPA2_PSK, password=self.config.get_passphrase())
            if not self.connection.active(): self.connection.active(True)
            
        starttime = time.time()
        lasttime = time.time()
        while timeout<(lasttime-starttime) and not self.connection.isconnected():
            lasttime = time.time()
            
        return self.connection.isconnected()
      
