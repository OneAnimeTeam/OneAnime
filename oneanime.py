#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from PIL import Image

project = 'OneAnime/2.0.1'


def read_file(filename, mode="r"):
    f = open(filename, mode)
    content = f.read()
    f.close()
    return content

style = {
    'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
    'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
    "none": 0
}
def log(state, message, color="none"):
    now_time = time.strftime("%Y/%m/%d %X", time.localtime())
    print("\033[{0}m{1} [{2}] {3}\033[0m".format(style[color], now_time, state, message))


def get_image(url):
    content = None
    hit_filename = None
    if os.path.isdir(url):
        if not url.endswith('/'):
            url += '/'
        files = []
        for filename in os.listdir(url):
            filename = url + filename
            if os.path.splitext(filename)[1] in ('.webp', '.jpg', '.jpeg', '.png'):
                files.append(filename)
        if len(files) != 0:
            hit_filename = random.choice(files)
    if os.path.isfile(url) and os.path.splitext(url)[1] in ('.webp', '.jpg', '.jpeg', '.png'):
        hit_filename = url
    #convert image to webp
    if hit_filename is not None and os.path.splitext(hit_filename)[1] in ('.jpg', '.jpeg', '.png'):
        new_filename = os.path.splitext(hit_filename)[0] + '.webp'
        Image.open(hit_filename).save(new_filename, "webp")
        os.remove(hit_filename)
        hit_filename=new_filename
        log("convert", 'Successfully converted the file "{0}" to webp'.format(os.path.basename(hit_filename)), "green")
    if hit_filename is not None:
        content = read_file(hit_filename, "rb")
        log("info", 'Hit the file: "{0}"'.format(os.path.basename(hit_filename)))
    return hit_filename, content


def error_string(error):
    strings = '<html><head><title>{0}</title></head><body><center><h1>{0}</h1><hr/><p>{1}</p></center></body></html>'.format(
        error, project)
    return strings


def send_request(self, response, content, length, filename=None):
    self.send_response(response)
    content_type = 'text/html'
    if response == 200:
        content_type = 'image/webp'
        self.send_header('Content-Disposition', 'inline;filename="{0}"'.format(filename))
    self.send_header('Content-type', content_type)
    self.send_header('Content-Length', length)
    self.send_header('Server', project)
    self.send_header('X-Powered-By', project)
    self.send_header('Conncetion', 'close')
    self.end_headers()
    self.wfile.write(content)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = location + self.path
        if url.find("?") != -1:
            split_url = url.split("?")
            url = split_url[0]
        filename, image = get_image(url)
        if image is None:
            content = error_string("404 Not Found")
            send_request(self, 404, bytes(content, encoding="utf-8"), len(content))
            return
        send_request(self, 200, image, len(image), os.path.basename(filename))



class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    config = json.loads(read_file("./config.json"))
    server_info = (config["server"], config["port"])
    location = config["location"]
    log("info", 'Serving OneAnime on {0}:{1} '.format(server_info[0], server_info[1]))
    server = ThreadingHTTPServer(server_info, RequestHandler)
    server.serve_forever()

