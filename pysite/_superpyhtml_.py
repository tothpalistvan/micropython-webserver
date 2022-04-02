# _superpyhtml_.py for pysite - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

try:
    import uos as os,gc
    MCUSERVER = True
except:
    import os
    MCUSERVER = False

class SuperPYHTML(object):
     
    def __init__(self, parent):
        self.conn = parent.connection
        self.cfg = parent.configuration
        self.RD = parent.HTTPRequestData
        self.Path = parent.path
        if self.Path[-1]!="/":
            self.Path += "/"
        self.PYFile = parent.pyfile
        self.GET = self.explode_RD( 'URLQuery', '=', '&' )
        self.POST = self.explode_RD( '_POST_', '=', '&' )
        self.Method = 'GET'
        if 'Method' in self.RD.keys():
            self.Method = self.RD['Method']
        self.tfn = self.Path + self.PYFile + '.tmpl'
        self.set_initialdata()
        
    def generate_menu(self):
        mh = ""
        for key in self.Menus:
            mi=self.Menus[key]
            mh += "<p>"
            if self.selm == mi['id']:
                mh += "<b>"
            mh += "<a href='" + mi['targeturl'] + "'>" + mi['title'] + "</a>"
            if self.selm == mi['id']:
                mh += "</b>"
            mh += "</p>"
        return mh
    
    def set_initialdata(self):
        self.Menus = {}
        self.Menus[0]= { 'id':0, 'title':'Welcome', 'targeturl':'pysite.py.html' }
        self.Menus[1]= { 'id':1, 'title':'Status', 'targeturl':'pysitestatus.py.html' }
        self.Menus[2]= { 'id':2, 'title':'Wifi', 'targeturl':'pysitewifi.py.html' }
        self.Menus[3]= { 'id':3, 'title':'I2C', 'targeturl':'pysite.py.html?menu=3' }
        sentdata = self.GET.copy()
        if self.Method == 'POST':
            sentdata = self.POST.copy()

        self.XD = {}
        self.XD.update(sentdata)
        self.data = self.PYFile

    def explode_RD(self, f, eqsep, isep):
        data = ''
        if f in self.RD.keys():
            data = self.RD[f]
        r = {}
        if data !='':
            dlist = data.split(isep)
            for d in dlist:
                item = d.split(eqsep)
                if len(item)==2:
                    r[item[0]]=item[1]
                else:
                    r[d]=d
        return r
            
    def doMCUThings(self):
        return True
    
    def fileExists(self,filename):
        try:
            return os.stat(filename)[6]
        except OSError:
            return False

    def generate_TMPLdata(self):
        self.XD['TMPLdata'] = 'Generated template File'
        r = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
        r+= '<html lang="en"><head>'
        r+= '<meta http-equiv="content-language" content = "en">'
        r+= '  <meta http-equiv="content-type" content="text/html; charset=UTF-8">'
        r+= '</head><body>'
        for key in self.XD:
            r+= '<p>' + key + ': {' + key + '}</p>'
        r+= '</body></html>'
        return r

    def read_TMPLfile(self, tfn):
        retval = False;
        if self.fileExists(tfn):
            f = open(tfn,'r')
            retval = f.read()
            f.close
        return retval        
                
    def generate(self):
        retval = self.read_TMPLfile(self.tfn)
        gc.collect()
        if retval == False:
            retval = self.generate_TMPLdata()
        try:
            return retval.format(**self.XD)
        except KeyError as e:
            return '<h1>Error - Not all variables were set!</h1>' + retval                    
            pass
        return self.data
