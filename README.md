# micropython-webserver
micropython-webserver for ESP-12F

This project is created because I would like to learn a bit programming in micropython on ESP-12F (8266EX) but I think you can use it in your home hobby project.

This a free software and it is distributed under the terms of the GNU General Public Licencense. So you have the right to copy, modify, redistribute as the GPL specified.

(c)2022 Tóthpál István <istvan@tothpal.eu>

Installation:
-------------

- If your ESP device haven't got micropython installed on it, first you have to install it.(https://micropython.org/download/esp8266/)
- You have to copy files from webserver folder to the root folder of ESP-12F micropython device.
- Create a '''html''' folder on your device and copy/create html files you would like to serve

Configuration:
--------------
- Currently at the `myconfiguration` you can specify your basic Wifi setting. Only "station mode" available now.

```
    def __init__(self):
        self.ssid = 'Your WIFI SSID'
        self.passphrase = 'Your Passphrase'
```

References:
-----------
https://docs.micropython.org/en/latest/esp8266/tutorial/ \
https://docs.micropython.org/en/latest/esp8266/tutorial/network_tcp.html

https://github.com/micropython/micropython/blob/master/examples/network/http_server.py
