class myPYHTMLContent(object):
    
    def __init__(self, config, RequestData, path, pyfile):
        self.configuration = config
        self.RequestData = RequestData
        self.Path = path
        if path[-1]!="/":
            self.Path += "/"
        self.PYFile = pyfile
        self.set_initialdata()
        
    def set_initialdata(self):
        self.somedata = 'Data'
        return True
        
    def doMCUThings(self):
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
        return content
