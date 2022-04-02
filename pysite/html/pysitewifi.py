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
        self.tfn = self.Path + 'pysite.tmpl'
        self.selm = 2

        c = '<h1>WIFI</h1>'
        c+= '<p>IP: %s</p>' % self.conn.get_address()
        c+= '<p>Netmask: %s</p>' % self.conn.get_netmask()
        c+= '<p>DNS: %s</p>' % ', '.join(self.conn.get_nameservers())
            
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
                if 'WIFI' in self.POST.keys():
                    if self.POST['WIFI'] == "Scan":
                        c = "<hr><p>Scan result:</p><pre class=\"ml30\">"
                        try:
                            aps = self.conn.scan()
                        except Exception as e:
                            import sys
                            sys.print_exception(e)
                            aps = []
                            pass
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
                c = '<form action="%s.py.html" method="post">' % self.PYFile
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
                del c
        return True
