# myconfiguration.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

class myConfiguration:

    def __init__(self):
        self.ssid = 'Your WIFI SSID'
        self.passphrase = 'Your Passphrase'
        print("myconfig init...")

    def get_ssid(self):
        return self.ssid
    
    def get_passphrase(self):
        return self.passphrase
