# mywebserver.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

import uos,usocket as socket,sys,gc,time

class myWebServer:

    def __init__(self, connection, configuration):
        self.configuration = configuration
        self.HTMLBasePath = self.configuration.getHTMLBasePath()
        self.DefaultFile = self.configuration.getDefaultFile()
        self.connection = connection
        self.HTTPRequestData = {}
        message = ''
        
        if not self.connection.isconnected():
            if not self.connection.connect(True, 30):
                message = 'Error - No connection!'
        if self.connection.isconnected():
            message = self.connection.get_address()
        
        print("myWebServer init...", message)

    def explode_data(self, data):
        """Explode HTTP Request Data
           Returns URI path + URIFile"""
        result = {}
        rows =  str(data).split("'")[1].split("\\r\\n")
        i = -1
        for row in rows:
            items = row.split(': ')
            if len(items)==1 and row!="":
                item = items[0].split()
                if item[0] in ['GET','HEAD','POST','PUT','DELETE','CONNECT','OPTIONS','TRACE','PATCH']:
                    result['Method'] = item[0]
                    result['URI'] = item[1]
                    result['HTTPver'] = item[2]
            elif len(items)==2:
                result[items[0]] = items[1]
            else:
                if row!="":
                    result[str(i)] = row
                    i -= 1
        self.HTTPRequestData = result

        poststart = str(data).rfind("\\r\\n")
        if poststart+4 < len(str(data)):
            self.HTTPRequestData['_POST_'] = str(data)[poststart+4:-1]

        if 'URI' in self.HTTPRequestData.keys():
            uri = self.HTTPRequestData['URI'].split('?')
            if isinstance(uri,list):
                self.HTTPRequestData['URIFile'] = uri[0]
                if len(uri)==2:
                     self.HTTPRequestData['URLQuery'] = uri[1]
            else:
                self.HTTPRequestData['URIFile'] = uri
                del self.HTTPRequestData['URLQuery']
            return self.HTTPRequestData['URIFile']
        return ''

    def fileExists(self,filename):
        try:
            uos.stat(filename)
            return True;
        except OSError:
            return False

    def isdir(self,filename):
        try:
           return uos.stat(filename)[0] & 0x4000
        except OSError:
           return False

    
    def start(self):       
#        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mysock = socket.socket()
        
        ai = socket.getaddrinfo(self.connection.get_address(), self.connection.get_port())
        addr = ai[0][-1]

        self.mysock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mysock.bind(addr)
        self.mysock.listen(5)
        while True:
          res = self.mysock.accept()
          conn = res[0]
          client_addr = res[1]

          req = conn.readline()
          retval = req
          while True:
              h = conn.readline()
              retval += h
              if h == b"" or h == b"\r\n":
                    break

          request = retval
          
          #print(request)
          if request:
              status = "ok"
              response = ""
              message = ""
              gc.collect()
              uri = self.explode_data(request)
              if 'Method' in self.HTTPRequestData.keys() and status=="ok":
                  if self.HTTPRequestData['Method'] not in ['GET','POST']:
                      status = "error"
                      response = "405 Method Not Allowed"
                      message = "HTTP/1.1 405 Method Not Allowed\n"
                  if self.HTTPRequestData['Method']=='POST':
                      #receive post data Content-Length
                      retval = conn.read(eval(self.HTTPRequestData['Content-Length']))
                      self.HTTPRequestData['_POST_'] = retval.decode()
              else:
                      status = "error"
                      response = "405 Method Not Allowed"
                      message = "HTTP/1.1 405 Method Not Allowed\n"

              if 'HTTPver' in self.HTTPRequestData.keys() and status=="ok":
                  if self.HTTPRequestData['HTTPver'] not in ['HTTP/1.0','HTTP/1.1']:
                      status = "error"
                      response = "505 HTTP Version Not Supported"
                      message = "HTTP/1.1 505 HTTP Version Not Supported\n"

#              print(len(request),len(retval),self.HTTPRequestData)

              if status=="ok":      
                accept = self.HTTPRequestData['Accept'].split(',')
        
                filename = self.HTMLBasePath + uri
              
                if self.isdir(filename):
                  if filename[-1] != "/":
                      filename += "/"
                  filename = filename+self.DefaultFile
                else:
                  if 'Referer' in self.HTTPRequestData.keys():
                    refer = self.HTTPRequestData['Referer'].split(self.HTTPRequestData['Host'])
                    if not self.fileExists(filename) and len(refer)==2:
                        if self.isdir(refer[1].split('?')[0]):
                            filename = self.HTMLBasePath + refer[1].split('?')[0] + uri
                        else:
                            cutpoint = refer[1].split('?')[0].rfind("/")
                            filename = self.HTMLBasePath + refer[1].split('?')[0][:cutpoint] + uri

                if filename[-8:] == ".py.html":
                  filename = filename[:-5]
                if self.fileExists(filename): 
                  if filename[-3:] == ".py":
                    #print( self.HTTPRequestData )
                    cutpoint = filename.rfind("/")
                    path = filename[:cutpoint]
                    pyfile = filename[cutpoint+1:-3] 
                    sys.path.append(path)
                    mymodules = __import__(pyfile, globals(), locals(), [], 0)
#                    print(mymodules)
                    pyhtml = mymodules.myPYHTMLContent(self.configuration, self.HTTPRequestData, path, pyfile)
                    sys.path.remove(path)
                    r = pyhtml.doMCUThings()
                    #if r==False:
                    response = pyhtml.generate()
                    del sys.modules[pyfile]
                    del pyhtml
                    del mymodules
                    gc.collect()
                  else:
                    f = open( filename )
                    response = f.read()
                    f.close()

                  #print(gc.mem_free())
                    
                  message = 'HTTP/1.1 200 OK\n'
                else:       
                  message = 'HTTP/1.1 404 Not Found\n'
                  response = 'HTTP 404 - File not found!'

              conn.write(message.encode())
              if status=="ok":
                  conn.write(('Content-Type: '+accept[0]+'\n').encode())
              else:
                  conn.write('Content-Type: text/html\n'.encode())
              conn.write( ('Content-Length: {}\n').format(len(response.encode())).encode())
              conn.write('Connection: close\n\n'.encode())
              conn.write(response.encode())
                  
          conn.close()
