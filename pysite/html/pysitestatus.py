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
        self.selm = 1

        c = "<h1>Status</h1>"
            
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
                tzd = self.cfg.tzd
                if 'STATUS' in self.POST.keys():
                    if 'tzd' in self.POST.keys():
                        try:
                            tzd = int(self.POST['tzd'])
                        except:
                            tzd = 0
                            pass
                    st = self.POST['STATUS']
                    if st == "Set+Time":
                        from machine import RTC
                        try:
                            d = self.POST['date'].split("-")
                            t = self.POST['time'].split("%3A")
                            RTC().datetime( (int(d[0]),int(d[1]),int(d[2]),0,int(t[0]),int(t[1]),int(t[2]),0) )
                        except:
                            pass
                    elif st == "NTP+Sync":
                        self.cfg.syncntp(tzd)
                    elif st == "Enable+NTP":
                        self.cfg.ntp = True
                        self.cfg.tzd = tzd
                        self.cfg.saveconfig()
                    elif st == "Disable+NTP":
                        self.cfg.ntp = False
                        self.cfg.tzd = tzd
                        self.cfg.saveconfig()
                    elif st == "Save":
                        self.cfg.tzd = tzd
                        self.cfg.saveconfig()
                t = time.localtime()
                wd = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][t[6]]
                c = "<p>Current time: %04d-%02d-%02d %02d:%02d:%02d %s</p>" % (t[0],t[1],t[2],t[3],t[4],t[5],wd)
                c+= '<form action="%s.py.html" method="post">' % self.PYFile
                c+= '  <p><label for="date">date: </label><input type="text" id="date" name="date" value="%04d-%02d-%02d"></p>' % (t[:3])
                c+= '  <p><label for="time">time: </label><input type="text" id="time" name="time" value="%02d:%02d:%02d"></p>' % (t[3:6])
                c+= '  <p><label for="tzd">taddon: </label><input type="text" id="tzd" name="tzd" value="%d"></p>' % tzd
                c+= '  <input name="STATUS" type="submit" value="Set Time">'
                c+= '  <input name="STATUS" type="submit" value="NTP Sync">'
                c+= '  <input name="STATUS" type="submit" value="%s NTP">' % ("Enable" if not self.cfg.ntp else "Disable")
                c+= '  <input name="STATUS" type="submit" value="Save">'
                c+= '</form><BR>'
                c+= "<p>Current configuration:</p><pre class=\"ml30\">"
                for it in self.cfg.__dict__:
                    c+= "<p>%s: %s</p>" % (it,self.cfg.__dict__[it])
                self.XD["MCUThings"]= c+"</pre>"
                del c
        return True
