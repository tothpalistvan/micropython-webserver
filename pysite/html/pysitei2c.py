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
        self.selm = 3
          
        self.XD.update( {
            "top": '<img style="float:left" src="TIS_mPy.jpg"><BR><h2 class=\"center\">Micropython webserver for ESP-12F</h2><hr style="clear:both">',
            "left": self.generate_menu(),
            "foot": "<hr><p class=\"center\">Example pySite addon to micropython-webserver by (c)2022 Tóthpál István</p>",
            } )

    def doMCUThings(self):
        self.XD['scan'] = "false"
        self.XD['dump'] = ""
        self.XD['i2ca'] = "0x50"
        c = ""
        title = self.Menus[self.selm]['title']
        
        if self.selm>=0 and self.selm<len(self.Menus):
            if MCUSERVER:
                if title == 'I2C':
                    from machine import Pin,I2C
                    i2c = I2C( scl=Pin(5),sda=Pin(4),freq=100000 )
                    if 'I2C' in self.POST.keys():
                        if self.POST['I2C'] in ["Scan","Dump"]:
                            s = i2c.scan()
                            self.XD['scan'] = "[%s]" % ",".join(["0x%02x" % x for x in s])
                            a = 0x50
                            if 'addr' in self.POST.keys():
                                a = int(self.POST['addr'])
                                self.XD['i2ca'] = a
                    if 'I2C' in self.POST.keys() and 'addr' in self.POST.keys():
                        if self.POST['I2C'] == "Dump":
                            if a in s:
                                for i in range(0,16):
                                    c+= "<p>%s</p>" % " ".join(["%02x" % x for x in i2c.readfrom_mem(a,i*16,16)])
                    self.XD["dump"] = c
        del c
        return True
