# mywebserver.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

import uos,usocket as socket,sys,gc,time

class myWebServer:

    def __init__(self, connection):
        self.connection = connection
        self.configuration = self.connection.get_configuration()
        self.HTMLBasePath = self.configuration.getHTMLBasePath()
        self.DefaultFile = self.configuration.getDefaultFile()
        self.HTTPRequestData = {}
        message = ''
        
        if not self.connection.isconnected():
            if (not self.connection.connect(True, 30)) and (self.configuration.wifimode == "station"):
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

    def receiveHTMLRequestHeader(self, connection):
        retval = connection.readline()
        while True:
            row = connection.readline()
            retval += row
            if row == b"" or row == b"\r\n":
                break
        return retval
    
    def handlePYHTMLfile(self, filename, connection, ctype):
        if self.fileExists(filename): 
            if filename[-3:] == ".py":
                cutpoint = filename.rfind("/")
                path = filename[:cutpoint]
                pyfile = filename[cutpoint+1:-3] 
                sys.path.append(path)
                mymodules = __import__(pyfile, globals(), locals(), [], 0)
                pyhtml = mymodules.myPYHTMLContent(self.configuration, self.HTTPRequestData, path, pyfile)
                sys.path.remove(path)
                r = pyhtml.doMCUThings()
                response = pyhtml.generate()
                del sys.modules[pyfile]
                del pyhtml
                del mymodules
            message = 'HTTP/1.1 200 OK\n'
        else:       
            message = 'HTTP/1.1 404 Not Found\n'
            response = 'HTTP 404 - File not found!'
        gc.collect()
 #       print(gc.mem_free())

        connection.write(message.encode())
        connection.write(('Content-Type: '+ctype+'\n').encode())
        connection.write( ('Content-Length: {}\n').format(len(response.encode())).encode())
        connection.write('Connection: close\n\n'.encode())
        connection.write(response.encode())
        
    # can it serve 32KB+ textfile??
    def serve_file(self, filename, connection, ctype):
        if self.fileExists(filename): 
            f = open( filename )
            response = f.read()
            f.close()                   
            message = 'HTTP/1.1 200 OK\n'
        else:       
            message = 'HTTP/1.1 404 Not Found\n'
            response = 'HTTP 404 - File not found!'
        gc.collect()
#        print(gc.mem_free())

        connection.write(message.encode())
        connection.write(('Content-Type: '+ctype+'\n').encode())
        connection.write( ('Content-Length: {}\n').format(len(response.encode())).encode())
        connection.write('Connection: close\n\n'.encode())
        connection.write(response.encode())
    
    def start(self):       
        while True:
          conn = self.mysock.accept()[0]
          request = self.receiveHTMLRequestHeader(conn)
         
          if request:
              status = "ok"
              response = ""
              message = ""
              gc.collect()
              print(gc.mem_free())
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
                        if self.isdir(refer[1].split('?')[0]):
                            filename = self.HTMLBasePath + refer[1].split('?')[0] + uri
                        else:
                            cutpoint = refer[1].split('?')[0].rfind("/")
                            filename = self.HTMLBasePath + refer[1].split('?')[0][:cutpoint] + uri

                if filename[-8:] == ".py.html":
                    self.handlePYHTMLfile(filename[:-5], conn, accept[0])
                else:
                    self.serve_file(filename, conn, accept[0])
              else:
                conn.write(message.encode())
                conn.write('Content-Type: text/html\n'.encode())
                conn.write( ('Content-Length: {}\n').format(len(response.encode())).encode())
                conn.write('Connection: close\n\n'.encode())
                conn.write(response.encode())
                  
          conn.close()

