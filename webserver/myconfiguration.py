# myconfiguration.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

class myConfiguration:

    def __init__(self):
        self.configfile = "myconfig.cfg"
        self.HTMLBasePath = "/html"
        self.DefaultFile = "index.html"
        self.Port = 80
        
        self.wifimode = 'AP'
        self.ssid = 'ESP12F-WIFI'
        self.passphrase = 'EspWifi1234'
        
        self.ntp = False
        self.tzd = 1

        cfg = self.loadconfig()
        
        if cfg!='':
            if 'server' in cfg.keys():
                if 'port' in cfg['server'].keys():
                    self.Port = cfg['server']['port']
                if 'htmlbasepath' in cfg['server'].keys():
                    self.HTMLBasePath = cfg['server']['htmlbasepath']
                if 'defaultfile' in cfg['server'].keys():
                    self.DefaultFile = cfg['server']['defaultfile']
            if 'wifi' in cfg.keys():
                if 'wifimode' in cfg['wifi'].keys():
                    self.wifimode = cfg['wifi']['wifimode']
                if 'ssid' in cfg['wifi'].keys():
                    self.ssid = cfg['wifi']['ssid']
                if 'passphrase' in cfg['wifi'].keys():
                    self.passphrase = cfg['wifi']['passphrase']
            if 'time' in cfg.keys():
                if 'ntp' in cfg['time'].keys():
                    self.ntp = cfg['time']['ntp']
                if 'tzd' in cfg['time'].keys():
                    self.tzd = cfg['time']['tzd']
        print("myconfig init...")

    def getHTMLBasePath(self):
        return self.HTMLBasePath
    
    def getDefaultFile(self):
        return self.DefaultFile
    
    def get_port(self):
        return self.Port

    def getWifiMode(self):
        return self.wifimode
    
    def get_ssid(self):
        return self.ssid
    
    def get_passphrase(self):
        return self.passphrase

    def saveconfig(self):
        cfg={}
        cfg['wifi'] = { "wifimode":self.wifimode, "ssid":self.ssid, "passphrase":self.passphrase }
        cfg['server'] = { "port":self.Port, "htmlbasepath":self.HTMLBasePath, "defaultfile":self.DefaultFile}
        cfg['time'] = { "ntp":self.ntp, "tzd":self.tzd }

        filedata = "{}".format(cfg)
        
        f = open( self.configfile, "w" )
        f.write(filedata)
        f.close()
        return True
    
    def loadconfig(self):
        cfg = ''
        try:
            f = open( self.configfile)
            filedata = f.read()
            f.close()
        
            cfg=eval(filedata)
        except:    
            pass
        
        return cfg

    def syncntp(self, tzd, tries=3):
        from machine import RTC
        import utime,ntptime
        t=0
        while t<tries:
            try:
                gmt = utime.localtime(ntptime.time())
                RTC().datetime( (gmt[0],gmt[1],gmt[2],gmt[6],gmt[3]+tzd,gmt[4],gmt[5],0) )
                break
            except Exception as e:
                import sys
                sys.print_exception(e)
                pass
            t+=1
