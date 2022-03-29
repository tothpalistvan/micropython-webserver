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
