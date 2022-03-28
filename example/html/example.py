# example.py - Example for micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>
from machine import Pin

class myPYHTMLContent(object):
    
    def __init__(self, parent):
        self.configuration = parent.configuration
        self.RequestData = parent.HTTPRequestData
        self.Path = parent.path
        if self.Path[-1]!="/":
            self.Path += "/"
        self.PYFile = parent.pyfile
        self.set_initialdata()
        
    def explode_post(self):
        post = ''
        retval = {}
        if '_POST_' in self.RequestData.keys():
            post = self.RequestData['_POST_']
        if post != '':
            plist = post.split('&')
            for p in plist:
                item = p.split('=')
                if len(item)==2:
                    retval[item[0]]=item[1]
                else:
                    retval[p]=p
        return retval

    def set_initialdata(self):
        self.POST = self.explode_post()
        
    def doMCUThings(self):
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
        return True
    
    def generate(self):
        query = ''
        if 'URLQuery' in self.RequestData.keys():
            query = self.RequestData['URLQuery']
        self.data = "ez valami"
        cookies = ''
        if 'Cookie' in self.RequestData.keys():
            cookies = self.RequestData['Cookie']

        content = "<h1>Welcome</h1>"
        content+= "<p>Query: "+ query +"</p>"
        content+= "<p>Posted: "+self.RequestData['_POST_']+"</p>"
        content+= "<p>Cookies: "+cookies+"</p>"
        content+= "<hr><p>Built-in LED state:" + self.LedState + "</p><BR>"

        content+= "<form action='"+self.PYFile+".py.html' method='post'>"
        content+= "  <input name='LED' type='submit' value='Turn On'>"
        content+= "  <input name='LED' type='submit' value='Turn Off'>"
        content+= "  <input name='LED' type='submit' value='Toggle'>"
        content+= "</form>"
        return content