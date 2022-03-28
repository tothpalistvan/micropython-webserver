# mywebserver.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

import uos,usocket as socket,sys,gc,time

class myWebServer:

    def __init__(self, connection):
        self.connection = connection
        self.configuration = self.connection.get_configuration()
        self.HTMLBasePath = self.configuration.getHTMLBasePath()
        self.DefaultFile = self.configuration.getDefaultFile()
        self.filepartsize = 1024
        self.HTTPRequestData = {}
        message = ''
        
        if not self.connection.isconnected():
            if (not self.connection.connect(True, 300)) and (self.configuration.wifimode == "station"):
                message = 'Error - No connection!'
        if self.connection.isconnected():
            message = self.connection.get_address()
        
        print("myWebServer init...", message)

        self.mysock = socket.socket()
       
        addr = socket.getaddrinfo(self.connection.get_address(), self.connection.get_port())[0][-1]

        self.mysock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mysock.bind(addr)
        self.mysock.listen(5)

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

        self.HTTPRequestData['_POST_'] = ''
        
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
            return uos.stat(filename)[6]
        except OSError:
            return False

    def isdir(self,filename):
        try:
           return uos.stat(filename)[0] & 0x4000
        except OSError:
           return False

    def receiveHTTPRequestHeader(self, connection):
        retval = connection.readline()
        while True:
            row = connection.readline()
            retval += row
            if row == b"" or row == b"\r\n":
                break
        return retval
    
    def sendHTTPAnswerHeader(self, connection, message, ctype, csize):
        connection.write(message.encode())
        connection.write(('Content-Type: '+ctype+'\n').encode())
        connection.write( ('Content-Length: {}\n').format(csize).encode())
        connection.write('Connection: close\n\n'.encode())
    
    def handlePYHTMLfile(self, filename, connection, ctype):
        if self.fileExists(filename): 
            if filename[-3:] == ".py":
                cutpoint = filename.rfind("/")
                self.path = filename[:cutpoint]
                self.pyfile = filename[cutpoint+1:-3] 
                sys.path.append(self.path)
                mymodules = __import__(self.pyfile, globals(), locals(), [], 0)
                pyhtml = mymodules.myPYHTMLContent( self )
                sys.path.remove(self.path)
                r = pyhtml.doMCUThings()
                response = pyhtml.generate()
                del sys.modules[self.pyfile]
                del pyhtml
                del mymodules
                del self.path
                del self.pyfile
            message = 'HTTP/1.1 200 OK\n'
        else:       
            message = 'HTTP/1.1 404 Not Found\n'
            response = 'HTTP 404 - File not found!'
        gc.collect()

        self.sendHTTPAnswerHeader(connection, message, ctype, len(response.encode()))
        connection.write(response.encode())
        
    # can it serve bin file?? - worked with jpg
    def serve_file(self, filename, connection, ctype):
        fsize=self.fileExists(filename)
        if fsize: 
            self.sendHTTPAnswerHeader(connection, 'HTTP/1.1 200 OK\n', ctype, fsize)

            f = open( filename )
            for i in range(0,fsize // self.filepartsize):
                response = f.read(self.filepartsize)
                connection.write(response.encode())
            response = f.read(fsize % self.filepartsize)
            connection.write(response.encode())
            f.close()
        else:       
            response = 'HTTP 404 - File not found!'
            self.sendHTTPAnswerHeader(connection, 'HTTP/1.1 404 Not Found\n', 'text/html', len(response.encode()))
            connection.write(response.encode())          
#        gc.collect()

    def start(self):       
        while True:
          conn = self.mysock.accept()[0]
          request = self.receiveHTTPRequestHeader(conn)
         
          if request:
              status = "ok"
              response = ""
              message = ""
              gc.collect()
#              print(gc.mem_free())
              uri = self.explode_data(request)
              if 'Method' in self.HTTPRequestData.keys() and status=="ok":
                  if self.HTTPRequestData['Method'] not in ['GET','POST']:
                      status = "error"
                      response = "405 Method Not Allowed"
                      message = "HTTP/1.1 405 Method Not Allowed\n"
                  if self.HTTPRequestData['Method']=='POST':
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
                        if self.isdir(self.HTMLBasePath + refer[1].split('?')[0]):
                            p = refer[1].split('?')[0]
                            if p[-1:]=="/" and uri[0]=="/":
                                p=p[:-1]
                            filename = self.HTMLBasePath + p + uri
                        else:
                            cutpoint = refer[1].split('?')[0].rfind("/")
                            p = refer[1].split('?')[0][:cutpoint]
                            if p[-1:]=="/" and uri[0]=="/":
                                p=p[:-1]
                            filename = self.HTMLBasePath + p + uri

                if filename[-8:] == ".py.html":
                    self.handlePYHTMLfile(filename[:-5], conn, accept[0])
                else:
                    self.serve_file(filename, conn, accept[0])
              else:
                self.sendHTTPAnswerHeader(conn, message, 'text/html', len(response.encode()))
                conn.write(response.encode())
                  
          conn.close()
