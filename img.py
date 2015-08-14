from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
import random,os,re
Guestnum=0
blocklist=[]
class Server(ThreadingMixIn, TCPServer): pass
class Handler(StreamRequestHandler):
     def handle(self):
          global Guestnum
          Guestnum=Guestnum+1
          print str(Guestnum)+' [Guest IP] :'+str(self.request.getpeername())
          data = self.request.recv(1024)
          self.wfile.write(Getimgfile(Getdirname(data),data))
              
def pngtojpg(filename):
  from wand.image import Image
  with Image(filename = filename) as img:
       filetemp=filename
       filename=filename.replace(".png",".jpg")
       img.save(filename = filename)
       os.remove(filetemp)
       return filename
def Getrefere(data):
    pat = re.compile('Referer: (.*?)\r\n',re.S)
    return pat.findall(data)
    
def Getdirname(data):
  headerList = data.split('\r\n')
  headerFirst = headerList[0]
  httpFirstItems = headerFirst.split(' ', 3)
  if len(httpFirstItems) <> 3:
       return "URL Error"
  else:
       httpUrl = httpFirstItems[1]
       if not httpUrl.endswith("/"):
            httpUrl=httpUrl+"/"
       return httpUrl

def outHttp(httpHeaderStat,httpContentType,contents):
    outs = httpHeaderStat
    outs += httpContentType
    outs += 'Server: OneAnime\r\n'
    outs += 'X-Powered-By: OneAnime1.0.4\r\n'
    outs += 'Content-Length: '+str(len(contents))+'\r\n'
    outs += 'Connection: close\r\n'
    outs += '\r\n'+contents
    return outs

def Getimgfile(httpUrl,data):
  print httpUrl
  if httpUrl <> "URL Error":
    blocken=False
    global blocklist
    if len(blocklist)<>0:
      referer=Getrefere(data)
      print "[Referer:"+referer+"]"
      if len(referer)<>0:
          for blocks in blocklist:
              if referer[0].find(blocks)<>0:
                 blocken=True
                 break 
    if blocken==False:
      if(os.path.isdir('.'+httpUrl)):
          httpHeaderStat = 'HTTP/1.1 200 OK\r\n'
          files=[]
          for filenames in os.listdir(os.path.dirname('.'+httpUrl)): 
               if filenames.endswith(".jpg") or filenames.endswith(".jpeg") or filenames.endswith(".png"):
                    files.append("."+httpUrl+filenames)
          try:
               filename=random.choice(files)
               if filename.endswith(".png"):
                   filename=pngtojpg(filename)
               print "[Return File:"+filename+"]"
               f = open(filename, 'rb')
               contents = f.read()
               f.close()
               if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    mimeType='image/jpeg'
               httpContentType = 'Content-Type: ' + mimeType + '\r\n'
          except:
               print "Loading Error"
               httpHeaderStat = 'HTTP/1.1 500 Internal Server Error\r\n'
               contents = """<html><head>
               <title>500 Internal Server Error</title>
               </head><body>
               <center><h1>500 Internal Server Error</h1></center>
               <hr><center><p>OneAnime/1.0.4</p></center>
               </body></html>"""
               httpContentType = 'Content-Type: text/html \r\n'
      else:
          httpHeaderStat = 'HTTP/1.1 404 Not Found\r\n'
          httpContentType = 'Content-Type: text/html \r\n'
          contents = """<html><head>
          <title>404 Not Found</title>
          </head><body>
          <center><h1>404 Not Found</h1></center>
          <center><p>The requested URL """+httpUrl+""" was not found on this server.</p></center>
          <hr><center><p>OneAnime/1.0.4</p></center>
          </body></html>"""
    else:
      httpHeaderStat = 'HTTP/1.1 200 OK\r\n'
      httpContentType = 'Content-Type: text/html \r\n'
      contents = """<html><head>
      <title>This Website is Already into blacklist</title>
      </head><body>
      <center><h1>This Website is Already into blacklist</h1></center>
      <hr><center><p>OneAnime/1.0.4</p></center>
      </body></html>"""
    return outHttp(httpHeaderStat,httpContentType,contents)

serverip=''
serverport=84
server = Server((serverip, serverport), Handler)
print 'Start OneAnime'
server.serve_forever()
