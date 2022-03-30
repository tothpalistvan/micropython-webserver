# Example pysite.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>
from _superpyhtml_ import SuperPYHTML,MCUSERVER

if MCUSERVER:
    from machine import Pin,I2C,RTC
    import utime as time
else:
    import time

class myPYHTMLContent(SuperPYHTML):
     
    def set_initialdata(self):
        super(myPYHTMLContent,self).set_initialdata()
        self.Menus[0]= { 'id':0, 'title':'Welcome', 'targeturl':self.PYFile+'.py.html' }
        self.Menus[1]= { 'id':1, 'title':'Status', 'targeturl':self.PYFile+'.py.html?menu=1' }
        self.Menus[2]= { 'id':2, 'title':'Wifi', 'targeturl':self.PYFile+'.py.html?menu=2' }
        self.Menus[3]= { 'id':3, 'title':'I2C', 'targeturl':self.PYFile+'.py.html?menu=3' }
        s = 0
        if 'menu' in self.GET.keys():
            try:
                s = int(self.GET['menu'])
            except:
                s = 0
                pass
        self.selectedmenu = s
        query = ''
        if 'URLQuery' in self.RD.keys():
            query = self.RD['URLQuery']
        cookies = ''
        if 'Cookie' in self.RD.keys():
            cookies = self.RD['Cookie']

        if self.selectedmenu>=0 and self.selectedmenu<len(self.Menus):
            title = self.Menus[self.selectedmenu]['title']
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
                c+= "<p>Cookies: "+cookies+"</p>"
            elif title == 'Status':
                c = "<h1>Status</h1>"
            elif title == 'Wifi':
                c = '<h1>WIFI</h1>'
                c+= '<p>IP: %s</p>' % self.conn.get_address()
                c+= '<p>Netmask: %s</p>' % self.conn.get_netmask()
                c+= '<p>DNS: %s</p>' % ', '.join(self.conn.get_nameservers())
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
        title = self.Menus[self.selectedmenu]['title']
        
        if self.selectedmenu>=0 and self.selectedmenu<len(self.Menus):
            if MCUSERVER:
                if title == 'Welcome':
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
                elif title == 'Status':
                    if 'STATUS' in self.POST.keys():
                        if self.POST['STATUS'] == "Set+Time":
                            try:
                                d = self.POST['date'].split("-")
                                t = self.POST['time'].split("%3A")
                                RTC().datetime( (eval(d[0]),eval(d[1]),eval(d[2]),0,eval(t[0]),eval(t[1]),eval(t[2]),0) )
                            except:
                                pass
                    t = time.localtime()[:6]
                    c = "<p>Current time: %04d-%02d-%02d %02d:%02d:%02d</p>" % t
                    c+= '<form action="%s.py.html?menu=%d" method="post">' % (self.PYFile,self.selectedmenu)
                    c+= '  <p><label for="date">date: </label><input type="text" id="date" name="date" value="%04d-%02d-%02d"></p>' % (t[:3])
                    c+= '  <p><label for="time">time: </label><input type="text" id="time" name="time" value="%02d:%02d:%02d"></p>' % (t[3:])
                    c+= '  <input name="STATUS" type="submit" value="Set Time">'
                    c+= '</form><BR>'
                    c+= "<p>Current configuration:</p><pre class=\"ml30\">"
                    for it in self.cfg.__dict__:
                        c+= "<p>%s: %s</p>" % (it,self.cfg.__dict__[it])
                    self.XD["MCUThings"]= c+"</pre>"
                elif title == 'Wifi':
                    if 'WIFI' in self.POST.keys():
                        if self.POST['WIFI'] == "Scan":
                            c = "<hr><p>Scan result:</p><pre class=\"ml30\">"
                            aps = self.conn.scan()
                            for item in aps:
                                mac = ":".join([hex(byte)[2:] for byte in item[1]])
                                c += "<p>%s : %d</p>" % (mac if item[5] else item[0].decode(),item[3])
                            self.XD["MCUThings"] = c + "</pre>"
                        if self.POST['WIFI'] == "Save":
                            self.cfg.wifimode=self.POST['wifimode']
                            self.cfg.ssid=self.POST['ssid']
                            self.cfg.passphrase=self.POST['psk']
                            self.cfg.saveconfig()
                            self.XD["MCUThings"]+= 'Configuration saved... Please, restart server manualy'
                    c = '<form action="%s.py.html?menu=%d" method="post">' % (self.PYFile,self.selectedmenu)
                    c+= '  <p><label for="wifimode">Wifi mode: </label><select id="wifimode" name="wifimode">'
                    c+= '    <option value="AP"%s>AP</option>' % (' selected=1' if self.cfg.wifimode=='AP' else '')
                    c+= '    <option value="station"%s>Station</option>' % (' selected=1' if self.cfg.wifimode=='station' else '')
                    c+= '  </select></p>'
                    c+= '  <p><label for="ssid">SSID: </label><input type="text" id="ssid" name="ssid" value="%s"></p>' % self.cfg.ssid
                    c+= '  <p><label for="psk">PSK: </label><input type="text" id="psk" name="psk" value="%s"></p>' % self.cfg.passphrase
                    c+= '  <input name="WIFI" type="submit" value="Save">'
                    c+= '  <input name="WIFI" type="submit" value="Scan">'
                    c+= '</form><BR>'
                    self.XD["MCUThings"]= c+self.XD["MCUThings"]
                elif title == 'I2C':
                    i2c = I2C( scl=Pin(5),sda=Pin(4),freq=100000 )
                    self.XD["MCUThings"] = "<hr><p>I2C scan: {}</p>".format(i2c.scan())
        return True
