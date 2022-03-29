# _superpyhtml_.py for pysite - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

try:
    import uos as os
    MCUSERVER = True
except:
    import os
    MCUSERVER = False

class SuperPYHTML(object):
     
    def __init__(self, parent):
        self.connection = parent.connection
        self.configuration = parent.configuration
        self.RequestData = parent.HTTPRequestData
        self.Path = parent.path
        if self.Path[-1]!="/":
            self.Path += "/"
        self.PYFile = parent.pyfile
        self.GET = self.explode_RequestData( 'URLQuery', '=', '&' )
        self.POST = self.explode_RequestData( '_POST_', '=', '&' )
        self.Method = 'GET'
        if 'Method' in self.RequestData.keys():
            self.Method = self.RequestData['Method']
        self.set_initialdata()
        
    def set_initialdata(self):
        sentdata = self.GET.copy()
        if self.Method == 'POST':
            sentdata = self.POST.copy()

        self.ExchangeData = {}
        self.ExchangeData.update(sentdata)
        self.data = self.PYFile

    def explode_RequestData(self, field, equationseparator, itemseparator):
        data = ''
        if field in self.RequestData.keys():
            data = self.RequestData[field]
        retval = {}
        if data !='':
            dlist = data.split(itemseparator)
            for d in dlist:
                item = d.split(equationseparator)
                if len(item)==2:
                    retval[item[0]]=item[1]
                else:
                    retval[d]=d
        return retval
            
    def doMCUThings(self):
        return True
    
    def fileExists(self,filename):
        try:
            os.stat(filename)
            return True;
        except OSError:
            return False

    def generate_TMPLdata(self):
        self.ExchangeData['TMPLdata'] = 'Generated template File'
        retval = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
        retval+= '<html lang="en">'
        retval+= '<head>'
        retval+= '<meta http-equiv="content-language" content = "en">'
        retval+= '  <meta http-equiv="content-type" content="text/html; charset=UTF-8">'
        retval+= '</head>'
        retval+= '<body>'

        for key in self.ExchangeData:
            retval+= '<p>' + key + ': {' + key + '}</p>'
            
        retval+= '</body>'
        retval+= '</html>'
        return retval        

    def read_TMPLfile(self, tmplfilename):
        retval = False;
        if self.fileExists(tmplfilename):
            f = open(tmplfilename)
            retval = f.read()
            f.close
        return retval        
                
    def generate(self):
        tmplfilename = self.Path + self.PYFile + '.tmpl'
        retval = self.read_TMPLfile(tmplfilename)
        if retval == False:
            retval = self.generate_TMPLdata()
        try:
            html = str(retval).format(**self.ExchangeData)
            return html
        except KeyError as e:
            return '<h1>Error - Not all variables were set!</h1>' + retval                    
            pass
        return self.data
