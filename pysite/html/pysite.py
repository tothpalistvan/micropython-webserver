# Example pysite.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>
from _superpyhtml_ import SuperPYHTML,MCUSERVER

if MCUSERVER:
    import utime as time
else:
    import time

class myPYHTMLContent(SuperPYHTML):
    
    def set_initialdata(self):
        super(myPYHTMLContent,self).set_initialdata()
        s = 0
        if 'menu' in self.GET.keys():
            try:
                s = int(self.GET['menu'])
            except:
                s = 0
                pass
        self.selm = s if s in [0,3] else 0
        query = ''
        if 'URLQuery' in self.RD.keys():
            query = self.RD['URLQuery']
        cookies = ''
        if 'Cookie' in self.RD.keys():
            ck = self.explode_RD( 'Cookie', '=', '; ' )

        if self.selm>=0 and self.selm<len(self.Menus):
            title = self.Menus[self.selm]['title']
            if title == 'Welcome':
                c = "<h1>Welcome"
                if self.POST != {}:
                    c+= (" " + self.POST['fname'] if 'fname' in self.POST.keys() else "")
                    c+= (" " + self.POST['lname'] if 'lname' in self.POST.keys() else "") 
                else:
                    if self.GET != {}:
                        c+= (" " + self.GET['fname'] if 'fname' in self.GET.keys() else "")
                        c+= (" " + self.GET['lname'] if 'lname' in self.GET.keys() else "")
                c+= "</h1>"
                c+= "<p>This is just an example page, You can see, how HTML data handled:</p>"
                c+= "<p>Query: "+ query +"</p>"
                c+= "<p>Posted: "+self.RD['_POST_']+"</p>"
                c+= "<p>Cookies:</p><pre class=\"ml30\">"
                for k in ck:
                    c+= "<p>%s = %s</p>" % (k,ck[k])
                c+= "</pre>"
            elif title == 'I2C':
                c = "<h1>I2C</h1>"
        else:
            content = "Invalid menu! - No Data!"
            
        self.XD.update( {
            "top": '<img style="float:left" src="TIS_mPy.jpg"><BR><h2 class=\"center\">Micropython webserver for ESP-12F</h2><hr style="clear:both">',
            "left": self.generate_menu(),
            "content": c,
            "foot": "<hr><p class=\"center\">Example pySite addon to micropython-webserver by (c)2022 Tóthpál István</p>",
            } )

    def doMCUThings(self):
        self.XD["MCUThings"]=""
        title = self.Menus[self.selm]['title']
        
        if self.selm>=0 and self.selm<len(self.Menus):
            if MCUSERVER:
                if title == 'Welcome':
                    from machine import Pin
                    LED = Pin(2, Pin.IN)
                    if 'LED' in self.POST.keys():
                        val = LED.value()
                        LED = Pin(2, Pin.OUT)
                        if self.POST['LED'] == "Turn+On":
                            LED.value(0)
                        elif self.POST['LED'] == "Turn+Off":
                            LED.value(1)
                        elif self.POST['LED'] == "Toggle":
                            LED.value((val+1) % 2)
                    self.LedState = "off" if LED.value() else "on"
                    c = "<hr><p>Built-in LED state:" + self.LedState + "</p><BR>"
                    c+= "<form action='"+self.PYFile+".py.html' method='post'>"
                    c+= "  <input name='LED' type='submit' value='Turn On'>"
                    c+= "  <input name='LED' type='submit' value='Turn Off'>"
                    c+= "  <input name='LED' type='submit' value='Toggle'>"
                    self.XD["MCUThings"]+= c+"</form><BR>"
                    del c
                elif title == 'I2C':
                    from machine import Pin,I2C
                    i2c = I2C( scl=Pin(5),sda=Pin(4),freq=100000 )
                    self.XD["MCUThings"] = "<hr><p>I2C scan: {}</p>".format(i2c.scan())
        return True
