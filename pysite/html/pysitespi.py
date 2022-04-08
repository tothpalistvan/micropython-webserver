# Example pysitei2c.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>
from _superpyhtml_ import SuperPYHTML,MCUSERVER

if MCUSERVER:
    import utime as time
else:
    import time

class myPYHTMLContent(SuperPYHTML):
    
    def set_initialdata(self):
        super(myPYHTMLContent,self).set_initialdata()
        self.tfn = self.Path + 'pysite.tmpl'
        self.selm = 4
          
        c = "<h1>SPI</h1>"
        c+= "<p>Trying to read AT25 flash (e.g. AT25DF321A) Manufacturer ID using sck=Pin(14),mosi=Pin(13),miso=Pin(12),cs=Pin(16)</p><hr>"

        self.XD.update( {
            "top": '<img style="float:left" src="TIS_mPy.jpg"><BR><h2 class=\"center\">Micropython webserver for ESP-12F</h2><hr style="clear:both">',
            "left": self.generate_menu(),
            "content": c,
            "foot": "<hr><p class=\"center\">Example pySite addon to micropython-webserver by (c)2022 Tóthpál István</p>",
            } )

    def doMCUThings(self):
        self.XD["MCUThings"]=""
        c = ""
        title = self.Menus[self.selm]['title']
        
        if self.selm>=0 and self.selm<len(self.Menus):
            if MCUSERVER:
                if title == 'SPI':
                    from machine import Pin,SoftSPI
                    spi = SoftSPI(baudrate=40000,sck=Pin(14),mosi=Pin(13),miso=Pin(12))
                    cs = Pin(16,Pin.OUT)
                    cs(0)
                    rx = bytearray(4)
                    spi.write(b'\x9f')
                    rx = spi.read(4,0)
                    cs(1)
                    self.XD["MCUThings"]=" ".join([("0x%02x" % x) for x in rx])
        del c
        return True
