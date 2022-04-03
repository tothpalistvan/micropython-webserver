Install:
--------
Just copy the html folder to root of your ESP device. Don't forget to copy the webserver too.


Your py code:
-------------
As you can see in example.py you have to create an object on the predefined name: `myPYHTMLContent`

You have to add/implement methods: 
```
class myPYHTMLContent(object):
  def __init__(self, server):
  '''Init'''
  
  def doMCUThings(self):
  '''Do something in MCU - e.g. change LED state'''
  
  def generate(self):
  '''Generate answer/result HTML'''
```

Don't forget that basicly your device has only 32KB RAM to use, so do not create to big files.

Another way, when you are using tmpl file like in pysite:


```
class SuperPYHTML(object):
     
    def __init__(self, parent):
        self.Path = parent.path
        if self.Path[-1]!="/":
            self.Path += "/"
        self.PYFile = parent.pyfile
        self.XD = {}
        self.tfn = self.Path + self.PYFile + '.tmpl'
        '''And generate self.XD[keys] - the exchange data in tmpl file'''
        
    def get_tmplfn(self):
        return self.tfn     

    def doMCUThings(self):
    '''Do something in MCU - e.g. change LED state
    And generate remaining self.XD[keys] - the exchange data in tmpl file'''
    
    def get_XD(self):
        return self.XD
```
The tmpl file is a HTML file with `{keys}` patterns. Each pattern like this will be changed to value of each `self.XD[keys]`.
