# Example pysite.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>
from _superpyhtml_ import SuperPYHTML,MCUSERVER

if MCUSERVER:
    from machine import Pin,I2C
    import utime as time
else:
    import time

class myPYHTMLContent(SuperPYHTML):
     
    def generate_menu(self):
        menuhtml = ""
        for key in self.Menus:
            menuitem=self.Menus[key]
            menuhtml += "<p>"
            if self.selectedmenu == menuitem['id']:
                menuhtml += "<b>"
            menuhtml += "<a href='" + menuitem['targeturl'] + "'>" + menuitem['title'] + "</a>"
            if self.selectedmenu == menuitem['id']:
                menuhtml += "</b>"
            menuhtml += "</p>"
        return menuhtml;
    
    def set_initialdata(self):
        super(myPYHTMLContent,self).set_initialdata()
        
        self.Menus = {}
        self.Menus[0]= { 'id':0, 'title':'Welcome', 'targeturl':self.PYFile+'.py.html' }
        self.Menus[1]= { 'id':1, 'title':'Status', 'targeturl':self.PYFile+'.py.html?menu=1' }
        self.Menus[2]= { 'id':2, 'title':'Wifi', 'targeturl':self.PYFile+'.py.html?menu=2' }
        self.Menus[3]= { 'id':3, 'title':'I2C', 'targeturl':self.PYFile+'.py.html?menu=3' }
        self.selectedmenu = 0
        if 'menu' in self.GET.keys():
                self.selectedmenu = int(self.GET['menu'])
        query = ''
        if 'URLQuery' in self.RequestData.keys():
            query = self.RequestData['URLQuery']
        cookies = ''
        if 'Cookie' in self.RequestData.keys():
            cookies = self.RequestData['Cookie']

        if self.selectedmenu>=0 and self.selectedmenu<len(self.Menus):
            if self.Menus[self.selectedmenu]['title'] == 'Welcome':
                content = "<h1>Welcome"
                if self.POST != {}:
                    content+= (" " + self.POST['fname'] if 'fname' in self.POST.keys() else "")
                    content+= (" " + self.POST['lname'] if 'lname' in self.POST.keys() else "") 
                else:
                    if self.GET != {}:
                        content+= (" " + self.GET['fname'] if 'fname' in self.GET.keys() else "")
                        content+= (" " + self.GET['lname'] if 'lname' in self.GET.keys() else "")
                content+= "</h1>"

                content+= "<p>This is just an example page, You can see, how HTML data handled:</p>"

                content+= "<p>Query: "+ query +"</p>"
                content+= "<p>Posted: "+self.RequestData['_POST_']+"</p>"
                content+= "<p>Cookies: "+cookies+"</p>"
            elif self.Menus[self.selectedmenu]['title'] == 'Status':
                content = "<h1>Status</h1>"
                content+= "<p>Current time: %04d-%02d-%02d %02d:%02d:%02d</p>" % time.localtime()[:6]
                content+= self.configuration.tohtml()
            elif self.Menus[self.selectedmenu]['title'] == 'Wifi':
                content = '<h1>WIFI</h1>'
                content+= '<p>IP: %s</p>' % self.connection.get_address()
                content+= '<p>Netmask: %s</p>' % self.connection.get_netmask()
                content+= '<p>DNS: %s</p>' % ', '.join(self.connection.get_nameservers())
                content+= '<form action="%s.py.html?menu=%d" method="post">' % (self.PYFile,self.selectedmenu)
                content+= '  <p><label for="wifimode">Wifi mode: </label><select id="wifimode" name="wifimode">'
                content+= '    <option value="AP"%s>AP</option>' % (' selected=1' if self.configuration.wifimode=='AP' else '')
                content+= '    <option value="station"%s>Station</option>' % (' selected=1' if self.configuration.wifimode=='station' else '')
                content+= '  </select></p>'
                content+= '  <p><label for="ssid">SSID: </label><input type="text" id="ssid" name="ssid" value="%s"></p>' % self.configuration.ssid
                content+= '  <p><label for="psk">PSK: </label><input type="text" id="psk" name="psk" value="%s"></p>' % self.configuration.passphrase
                content+= '  <input name="WIFI" type="submit" value="Save">'
                content+= '  <input name="WIFI" type="submit" value="Scan">'
                content+= '</form><BR>'
            elif self.Menus[self.selectedmenu]['title'] == 'I2C':
                content = "<h1>I2C</h1>"
        else:
            content = "Invalid menu! - No Data!"
            
        self.ExchangeData.update( {
            "top": '<img style="float:left" src="TIS_mPy.jpg"><BR><h2 class=\"center\">Micropython webserver for ESP-12F</h2><hr style="clear:both">',
            "left": self.generate_menu(),
            "content": content,
            "foot": "<hr><p class=\"center\">Example pySite addon to micropython-webserver by (c)2022 Tóthpál István</p>",
            } )

    def doMCUThings(self):
        self.ExchangeData["MCUThings"]=""
        
        if self.selectedmenu>=0 and self.selectedmenu<len(self.Menus):
            if MCUSERVER:
                if self.Menus[self.selectedmenu]['title'] == 'Welcome':
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
                    self.ExchangeData["MCUThings"] = "<hr><p>Built-in LED state:" + self.LedState + "</p><BR>"
                    self.ExchangeData["MCUThings"]+= "<form action='"+self.PYFile+".py.html' method='post'>"
                    self.ExchangeData["MCUThings"]+= "  <input name='LED' type='submit' value='Turn On'>"
                    self.ExchangeData["MCUThings"]+= "  <input name='LED' type='submit' value='Turn Off'>"
                    self.ExchangeData["MCUThings"]+= "  <input name='LED' type='submit' value='Toggle'>"
                    self.ExchangeData["MCUThings"]+= "</form><BR>"
                elif self.Menus[self.selectedmenu]['title'] == 'Wifi':
                    if 'WIFI' in self.POST.keys():
                        if self.POST['WIFI'] == "Scan":
                            self.ExchangeData["MCUThings"]+= "<hr>Scan result:"
                            aps = self.connection.scan()
                            for item in aps:
                                mac = ":".join([hex(byte)[2:] for byte in item[1]])
                                self.ExchangeData["MCUThings"] += "<p>%s : %d</p>" % (mac if item[5] else item[0].decode(),item[3])
                        if self.POST['WIFI'] == "Save":
                            self.configuration.wifimode=self.POST['wifimode']
                            self.configuration.ssid=self.POST['ssid']
                            self.configuration.passphrase=self.POST['psk']
                            self.configuration.saveconfig()
                            self.ExchangeData["MCUThings"]+= 'Configuration saved... Please, restart server manualy'
                elif self.Menus[self.selectedmenu]['title'] == 'I2C':
                    i2c = I2C( scl=Pin(5),sda=Pin(4),freq=100000 )
                    self.ExchangeData["MCUThings"] = "<hr><p>I2C scan: {}</p>".format(i2c.scan())
        return True
