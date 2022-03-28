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

    def get_configuration(self):
        return self.config

    def scan(self):
        if hasattr(self,'connection'):
            return self.connection.scan()
        return False      

    def get_netmask(self):
        if hasattr(self,'connection'):
            return self.connection.ifconfig()[1]
        return False      

    def get_nameservers(self):
        if hasattr(self,'connection'):
            return self.connection.ifconfig()[2:3]
        return False      

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
        