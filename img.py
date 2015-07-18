from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
import random
import os
Guestnum=0
class Server(ThreadingMixIn, TCPServer): pass
class Handler(StreamRequestHandler):
     def handle(self):
          global Guestnum
          Guestnum=Guestnum+1
          addr = self.request.getpeername()
          print str(Guestnum)+' [Guest IP] :', addr
          data = self.request.recv(1024)
          headerList = data.split('\r\n')
          headerFirst = headerList[0]
          httpFirstItems = headerFirst.split(' ', 3)
          if not len(httpFirstItems)==3:
               print "URL Error"
          else:
               httpUrl = httpFirstItems[1]
               if not httpUrl.endswith("/"):
                    httpUrl=httpUrl+"/"
               if(os.path.isdir('.'+httpUrl)):
                    httpHeaderStat = 'HTTP/1.1 200 OK\r\n'
                    files=[]
                    for filenames in os.listdir(os.path.dirname('.'+httpUrl)): 
                         if filenames.endswith(".jpg") or filenames.endswith(".jpeg") or filenames.endswith(".png"):
                              files.append("."+httpUrl+filenames)
                    try:
                         filename=random.choice(files)
                         if filename.endswith(".png"):
                              from wand.image import Image
                              with Image(filename = filename) as img:
                                   filetemp=filename
                                   filename=filename.replace(".png",".jpg")
                                   img.save(filename = filename)
                                   os.remove(filetemp)
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
                         <hr><center><p>OneAnime/1.0.3</p></center>
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
                    <hr><center><p>OneAnime/1.0.3</p></center>
                    </body></html>"""

               str_length = len(contents)
               outs  = httpHeaderStat
               outs += httpContentType
               outs += 'Server: OneAnime\r\n'
               outs += 'X-Powered-By: OneAnime1.0.3\r\n'
               outs += 'Content-Length: '+str(str_length)+'\r\n'
               outs += '\r\n'+contents
               self.wfile.write(outs)
serverip=''
serverport=84
server = Server((serverip, serverport), Handler)
print 'Start OneAnime'
server.serve_forever()
