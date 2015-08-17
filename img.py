from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
import random,os,re
Guestnum=0
whitelist=[]
Project_Name="OneAnime/1.0.4"
class Server(ThreadingMixIn, TCPServer): pass
class Handler(StreamRequestHandler):
     def handle(self):
          global Guestnum
          Guestnum=Guestnum+1
          print str(Guestnum)+' [Guest IP] :'+str(self.request.getpeername())
          data = self.request.recv(1024)
          self.wfile.write(Getdirname(data))
              
def pngtojpg(filename):
  from wand.image import Image
  with Image(filename = filename) as img:
       filetemp=filename
       filename=filename.replace(".png",".jpg")
       img.save(filename = filename)
       os.remove(filetemp)
       return filename

def drawwater(filename):
  from wand.font import Font
  font = Font(path ="./Inconsolata.otf",size=72)
  from wand.image import Image
  with Image(filename = filename) as image:
    image.caption('OneAnime', left=image.width-450, top=image.height-100, width=400, height=100, font=font)
    filename=filename+".temp"
    image.save(filename = filename)
    return filename
    
def Getrefere(data):
  pat = re.compile('Referer: (.*?)\r\n',re.S)
  return pat.findall(data)
    
def Getdirname(data):
  headerList = data.split('\r\n')
  headerFirst = headerList[0]
  httpFirstItems = headerFirst.split(' ', 3)
  global Project_Name
  global whitelist
  if len(httpFirstItems) <> 3:
       return "URL Error"
  else:
       httpUrl = httpFirstItems[1]
       if httpUrl == "/update_whitelist":
        Getwhitelist()
        httpHeaderStat = 'HTTP/1.1 200 OK\r\n'
        httpContentType = 'Content-Type: text/html\r\n'
        contents = """<html><head>
          <title>White list has been refreshed</title>
          </head><body>
          <center><h1>White list has been refreshed</h1></center>
          <hr><center><p>"""+Project_Name+"""</p></center>
          </body></html>"""
        return outHttp(httpHeaderStat,httpContentType,contents)
       if not httpUrl.endswith("/"):
          httpUrl=httpUrl+"/"
       return Getimgfile(httpUrl,data)

def Getwhitelist():
  global whitelist
  f = open("./whitelist.txt", 'rb')
  contents = f.read()
  f.close()
  whitelist=contents.split("|")
def outHttp(httpHeaderStat,httpContentType,contents):
  outs = httpHeaderStat
  outs += httpContentType
  outs += 'Server: OneAnime\r\n'
  outs += 'X-Powered-By: '+Project_Name+'\r\n'
  outs += 'Content-Length: '+str(len(contents))+'\r\n'
  outs += 'Connection: close\r\n'
  outs += '\r\n'+contents
  return outs

def Getfile(filename):
  global Project_Name
  try:
      f = open(filename, 'rb')
      contents = f.read()
      f.close()
      if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".temp"):
           mimeType='image/jpeg'
      httpHeaderStat = 'HTTP/1.1 200 OK\r\n'
      httpContentType = 'Content-Type: ' + mimeType + '\r\n'
  except:
        print "Loading Error"
        httpHeaderStat = 'HTTP/1.1 500 Internal Server Error\r\n'
        contents = """<html><head>
        <title>500 Internal Server Error</title>
        </head><body>
        <center><h1>500 Internal Server Error</h1></center>
        <hr><center><p>"""+Project_Name+"""</p></center>
        </body></html>"""
        httpContentType = 'Content-Type: text/html \r\n'
  return outHttp(httpHeaderStat,httpContentType,contents)
def Getimgfile(httpUrl,data):
  if httpUrl <> "URL Error":
    blocken=False
    global whitelist
    if len(whitelist) <> 0:
      referer=Getrefere(data)
      if len(referer) <> 0:
          print "[Referer:"+referer[0]+"]"
          for white in whitelist:
              if referer[0].find(white) <> -1:
                 blocken=True
                 break
    if(os.path.isdir('.'+httpUrl)):
      files=[]
      for filenames in os.listdir(os.path.dirname('.'+httpUrl)): 
           if filenames.endswith(".jpg") or filenames.endswith(".jpeg") or filenames.endswith(".png"):
                files.append("."+httpUrl+filenames)
    else:
        return print404(httpUrl)
    if blocken==False:
        if len(files) <> 0:
          filename=random.choice(files)
          if not os.path.isdir(filename+".temp"):
            filename=drawwater(filename)
          if filename.endswith(".png"):
              filename=pngtojpg(filename)
          print "[Return File:"+filename+"]"
          return Getfile(filename)
        else:
          return print404(httpUrl)
    else:
        if len(files) <> 0:
          filename=random.choice(files)
          if filename.endswith(".png"):
              filename=pngtojpg(filename)
          print "[Return File:"+filename+"]"
          return Getfile(filename)
        else:
          return print404(httpUrl)
def print404(httpUrl):
  global Project_Name
  httpHeaderStat = 'HTTP/1.1 404 Not Found\r\n'
  httpContentType = 'Content-Type: text/html \r\n'
  contents = """<html><head>
  <title>404 Not Found</title>
  </head><body>
  <center><h1>404 Not Found</h1></center>
  <center><p>The requested URL """+httpUrl+""" was not found on this server.</p></center>
  <hr><center><p>"""+Project_Name+"""</p></center>
  </body></html>"""
  return outHttp(httpHeaderStat,httpContentType,contents)

serverip=''
serverport=84
server = Server((serverip, serverport), Handler)
print 'Start OneAnime'
Getwhitelist()
server.serve_forever()