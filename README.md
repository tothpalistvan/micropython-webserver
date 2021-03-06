# micropython-webserver for ESP-12F
A simple HTTP server on your MCU, designed to use in <a target="_blank" href="https://github.com/tothpalistvan/micropython-webserver/blob/main/img/ESP12F.jpg" title="ESP-12F Wifi module">ESP-12F Wifi module</a>, but it may work with antoher micropython MCU-s (e.g ESP32).

There is an opportunity to run "server side script" to execute e.g. MCU commands in micropython. There is an example here how to do that. I'm creating another example called `pysite`.

This project is created because I would like to learn a bit programming in micropython on ESP-12F (8266EX) but I think you can use it in your home hobby project.

This a free software and it is distributed under the terms of the GNU General Public Licencense. So you have the right to copy, modify, redistribute as the GPL specified.

(c)2022 Tóthpál István <istvan@tothpal.eu>

Installation:
-------------

- If your ESP device hasn't got micropython installed on it, first you have to install it.(https://micropython.org/download/esp8266/)
- You have to copy files from webserver folder to the root folder of ESP-12F micropython device.
- Create a `html` folder on your device and copy/create html files you would like to serve

If you have installed `adafruit-ampy` you can use install shell scripts under Linux (e.g. `instserver.sh /dev/ttyUSB0`)

Configuration:
--------------
Currently at the `myconfiguration` you can specify the default basic settings.

```
    def __init__(self):
        self.configfile = "myconfig.cfg"
        self.HTMLBasePath = "/html"
        self.DefaultFile = "index.html"
        self.Port = 80
        
        self.wifimode = 'AP'
        self.ssid = 'ESP12F-WIFI'
        self.passphrase = 'EspWifi1234'

        self.ntp = False
        self.tzd = 1 #timezone addon (difference from GMT time with Daylight Savings)
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
    },
'time': {
    'ntp': True,
    'tzd': 2
    }
}
```

References:
-----------
https://docs.micropython.org/en/latest/esp8266/tutorial/ \
https://docs.micropython.org/en/latest/esp8266/tutorial/network_tcp.html

https://github.com/micropython/micropython \
https://github.com/micropython/micropython/blob/master/examples/network/http_server.py

https://www.ietf.org/rfc/rfc2616.txt \
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422

https://www.espressif.com/en/support/documents/technical-documents?keys=&field_type_tid%5B%5D=14 \
https://usermanual.wiki/Ai-Thinker-Technology/ESP12F
