# micropython-webserver
micropython-webserver for ESP-12F

This project is created because I would like to learn a bit programming in micropython on ESP-12F (8266EX) but I think you can use it in your home hobby project.

This a free software and it is distributed under the terms of the GNU General Public Licencense. So you have the right to copy, modify, redistribute as the GPL specified.

(c)2022 Tóthpál István <istvan@tothpal.eu>

Installation:
-------------

- If your ESP device hasn't got micropython installed on it, first you have to install it.(https://micropython.org/download/esp8266/)
- You have to copy files from webserver folder to the root folder of ESP-12F micropython device.
- Create a '''html''' folder on your device and copy/create html files you would like to serve

Configuration:
--------------
- Currently at the `myconfiguration` you can specify the default basic settings.

```
    def __init__(self):
        self.configfile = "myconfig.cfg"
        self.HTMLBasePath = "/html"
        self.DefaultFile = "index.html"
        self.Port = 80
        
        self.wifimode = 'AP'
        self.ssid = 'ESP12F-WIFI'
        self.passphrase = 'EspWifi1234'
```
But config file prefered, you can save one as `myconfig.cfg`:
```
{
'wifi': {
    'wifimode': 'station',
    'ssid': 'Your Wifi SSID', 
    'passphrase': 'Your passphrase'
    }, 
'server': { 
    'port': 80, 
    'htmlbasepath': '/html', 
    'defaultfile': 'index.html'
    }
}
```

References:
-----------
https://docs.micropython.org/en/latest/esp8266/tutorial/ \
https://docs.micropython.org/en/latest/esp8266/tutorial/network_tcp.html

https://github.com/micropython/micropython/blob/master/examples/network/http_server.py
