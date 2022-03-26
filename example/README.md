Install:
--------
Just copy the html folder to root of your ESP device. Dont forget to copy the webserver too.


Your py code:
-------------
As you can see in example.py you have to create an object on the predefined name: ''''myPYHTMLContent'''

You have to add/implement methods: '''__init__(self, RequestData, path, pyfile); doMCUThings(self); generate(self)'''

Don't forget that basicly your device has only 32KB RAM to use, so do not create to big files.
