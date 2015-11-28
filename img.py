#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

server_info = ('0.0.0.0', 8000)
font = './Inconsolata.otf'
watermark = 'OneAnime'
wl_enable = True

try:
    import wand
    wand_lib = True
except ImportError:
    wand_lib = False

class OneAnime():

    whitelist = []
    wand_lib = False
    font = ''
    watermark = 'OneAnime'
    wl_enable = True
    project = 'OneAnime/2.0.1'

    def __init__(self, wand_lib, font, watermark, wl_enable):
        self.wand_lib = wand_lib
        self.font = font
        self.watermark = watermark
        self.wl_enable = wl_enable

    def update_whitelist(self):
        import os
        filename = './whitelist.txt'
        if os.path.isfile(filename):
            f = open(filename)
            try:
                lines = f.readlines()
                lines = [line.strip('\r\n') for line in lines if line.strip()]
            except:
                lines = []
            finally:
                f.close()
        else:
            lines = []
        self.whitelist = lines
        return len(lines)

    def get_image(self, url, referer):
        import os
        import random
        url = '.' + url
        if not url.endswith('/'):
            url += '/'
        if os.path.exists(url):
            files = []
            for filename in os.listdir(url):
                filename = url + filename
                if os.path.splitext(filename)[1] in ('.jpg', '.jpeg', '.png') and self.wand_lib:
                    files.append(filename)
                elif os.path.splitext(filename)[1] in ('.jpg', '.jpeg'):
                    files.append(filename)
            if not files:
                return None
            filename = random.choice(files)
            print('[Return]: ', filename)
            return self._get_file(filename, referer)
        else:
            return ''

    def _get_file(self, filename, referer):
        import os
        if os.path.splitext(filename)[1] == '.png' and self.wand_lib:
            filename = self._png_to_jpg(filename)
            if filename is None:
                return None
        if not self._is_whitelisted(referer) and self.wl_enable and self.wand_lib:
            filename = self._watermark(filename)
            if filename is None:
                return None
        if os.path.isfile(filename):
            f = open(filename, 'rb')
            try:
                content = f.read()
            except:
                content = None
            finally:
                f.close()
            return content
        else:
            return None

    def _is_whitelisted(self, referer):
        import urllib
        if referer is None:
            return False
        proto, rest = urllib.splittype(referer)
        host, rest = urllib.splithost(rest)
        if [wl for wl in self.whitelist if wl == host]:
            return True
        return False

    def _watermark(self, filename):
        import os
        from wand.image import Image
        from wand.drawing import Drawing
        if not os.path.isfile(self.font):
            return filename
        if os.path.isfile(filename):
            with Drawing() as draw:
                with Image(filename = filename) as image:
                    draw.font = self.font
                    draw.font_size = 42
                    draw.text(50, 50, self.watermark)
                    draw(image)
                    image.format = 'jpeg'
                    filename = os.path.splitext(filename)[0] + '.temp'
                    image.save(filename=filename)
                    return filename
        else:
            return None

    def _png_to_jpg(self, filename):
        import os
        from wand.image import Image
        if os.path.isfile(filename):
            with Image(filename = filename) as image:
                image.format = 'jpeg'
                new_filename = os.path.splitext(filename)[0] + '.jpg'
                image.save(filename=new_filename)
                os.remove(filename)
                return new_filename
        else:
            return None

    def string_404(self, path):
        strings = [
            '<html><head>',
            '<title>404 Not Found</title></head>',
            '<body><center><h1>404 Not Found</h1>',
            'Cannot GET %s' % (path),
            '<hr /><p>%s</p></center></body></html>' % (self.project)
        ]
        return strings

    def string_500(self):
        strings = [
            '<html><head>',
            '<title>500 Internal Server Error</title></head>',
            '<body><center><h1>500 Internal Server Error</h1>',
            '<hr /><p>%s</p></center></body></html>' % (self.project)
        ]
        return strings

    def string_update(self, count):
        strings = [
            '<html><head>',
            '<title>Whitelist Refreshed</title></head>',
            '<body><center><h1>Whitelist Refreshed</h1>',
            '%s domain(s) has been loaded<hr />' % (str(count)),
            '<p>%s</p></center></body></html>' % (self.project)
        ]
        return strings


app = OneAnime(wand_lib, font, watermark, wl_enable)

class RequestHandler(BaseHTTPRequestHandler):

    global app

    def do_GET(self):
        referer = self.headers.get('Referer')
        ip = self.client_address[0]
        print('[Client IP]: ', ip)
        print('[Referer]: ', referer)
        if self.path == '/update':
            count = app.update_whitelist()
            print(count, 'domain(s) has been loaded')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            for line in app.string_update(count):
                self.wfile.write(line)
        else:
            image = app.get_image(self.path, referer)
            if image is None:
                print('[Error]: 500 Internal Server Error')
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                for line in app.string_500():
                    self.wfile.write(line)
            elif image == '':
                print('[Error]: 404 Not Found: ', self.path)
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                for line in app.string_404(self.path):
                    self.wfile.write(line)
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', str(len(image)))
                self.send_header('Server', app.project)
                self.send_header('X-Powered-By', app.project)
                self.send_header('Conncetion', 'close')
                self.end_headers()
                self.wfile.write(image)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    print(app.update_whitelist(), 'domain(s) has been loaded')
    print('Serving OneAnime on %s port %s ' % server_info)
    server = ThreadingHTTPServer(server_info, RequestHandler)
    server.serve_forever()
