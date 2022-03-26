# mywebserver.py - micropython-webserver - free sotware under GNU GPL
# Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

#
#   Now it can only serve HTML files, maybe it would be connected with custom python queries/MCU commands

import uos,socket

class myWebServer:

    def __init__(self, connection):
        self.connection = connection
        self.HTMLBasePath = "/html"
        self.DefaultFile = "index.html"
        message = ''
        
        if not self.connection.isconnected():
            if not self.connection.connect(True, 30):
                message = 'Error - No connection!'
        if self.connection.isconnected():
            message = self.connection.get_address()
        
        print("myWebServer init...", message)

    def explode_data(self, data):
        tmp = str(data).split("\\r\\n")[0].split()
        return tmp[1].split("?")

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
        addr = socket.getaddrinfo( self.connection.get_address(), 80)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(5)

        while True:
          conn, addr = s.accept() # addr = connection from address
          request = conn.recv(1024)
          if request:
              path = self.explode_data(request) 
              accept = str(request).split("\\r\\n")[3].split(": ")[1].split(",")
        
              if isinstance(path,list):
                filename = self.HTMLBasePath + path[0]
              else: 
                filename = self.HTMLBasePath + path
              
              if self.isdir(filename):
                if filename[-1] != "/":
                      filename += "/"
                filename = filename+self.DefaultFile
                  
              if self.fileExists(filename): 
                  f = open( filename )
                  response = f.read()
                  f.close()
        
                  conn.send('HTTP/1.1 200 OK\n')
                  conn.send('Content-Type: '+accept[0]+'\n')
                  conn.send('Connection: close\n\n')
                  conn.sendall(response)
              else:
                  conn.send('HTTP/1.1 404 Not Found\n')
                  conn.send('Content-Type: text/html\n')
                  conn.send('Connection: close\n\n')
                  conn.sendall('HTTP 404 - File not found!')
                  
          conn.close()
