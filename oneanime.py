#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import random
import signal
import time
import urllib.parse as url_parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

try:
    from PIL import Image
except ImportError:
    print("Please install the pillow package to support this feature")
    exit(1)

project = 'OneAnime'
server = None

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


def write_file(filename, content):
    f = open(filename, "w", newline=None)
    f.write(content)
    f.close()
    return True

def get_image(url, use_webp):
    result_type = ".webp"
    if not use_webp:
        result_type = ".jpgp"
    result_filename = None
    result_file = None
    if result_filename is None:
        files_convert = list()
        files_unconvert = list()
        if os.path.exists(url + "convert_list.json"):
            files_convert = json.loads(read_file(url + "convert_list.json"))
        dir_list = list()
        for filename in os.listdir(url):
            if os.path.splitext(filename)[1].lower() in ('.webp', '.jpgp', '.jpg', '.jpeg', '.png'):
                dir_list.append(filename)
                files_unconvert.append(os.path.splitext(filename)[0])
        files = files_convert+files_unconvert
        if len(files) != 0:
            hit_filename = random.choice(files)
            result_filename = hashlib.md5(str(hit_filename).encode('utf-8')).hexdigest()
            result_file = "{0}convert/{1}".format(url, result_filename)
            if hit_filename in files_unconvert:
                # convert image to webp
                unconvert_file = dir_list[files_unconvert.index(hit_filename)]
                if not os.path.isdir("{0}convert".format(url)):
                    os.mkdir("{0}convert".format(url))
                image = Image.open(url+unconvert_file)
                image = image.convert("RGB")
                image.save(result_file + ".webp", "webp")
                image.save(result_file + ".jpg", "JPEG")
                log("convert",
                    'Successfully converted the file "{0}" to webp and jpgp'.format(os.path.basename(hit_filename)),
                    "green")
                files_convert.append(hit_filename)
                write_file(url + "convert_list.json",json.dumps(files_convert))
                os.remove(url+unconvert_file)
    if result_filename is not None:
        content = read_file(result_file + result_type, "rb")
        log("info", 'Hit the file: "{0}"'.format(os.path.basename(result_filename + result_type)))
        return result_filename + result_type, content
    return None,None



def error_string(error):
    strings = '<html><head><title>{0}</title></head><body><center><h1>{0}</h1><hr/><p>{1}</p></center></body></html>'.format(
        error, project)
    return strings


def send_request(self, response, content, length, filename=None):
    self.send_response(response)
    content_type = 'text/html'
    if response == 200:
        content_type = 'image/jpeg'
        if os.path.splitext(filename)[1].lower() == ".webp":
            content_type = 'image/webp'
        self.send_header('Content-Disposition', 'inline;filename="{0}"'.format(url_parse.quote(filename, safe='')))
    self.send_header('Content-type', content_type)
    self.send_header('Content-Length', length)
    self.send_header('Server', project)
    self.send_header('X-Powered-By', project)
    self.send_header('Conncetion', 'close')
    self.end_headers()
    self.wfile.write(content)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        image = None
        filename = None
        use_webp = False
        url = location + url_parse.unquote(self.path)
        if url.find("?") != -1:
            split_url = url.split("?")
            url = split_url[0]
        if self.headers['accept'].find("image/webp") != -1:
            use_webp = True
        if url.endswith('.webp') or url.endswith(".jpgp"):
            path = os.path.dirname(url)
            filename = os.path.basename(url)
            filename_path="{0}/convert/{1}".format(path, filename)
            if os.path.exists(filename_path):
                image = read_file(filename_path,"rb")
        if os.path.exists(url) and image is None:
            if not url.endswith('/'):
                url += '/'
            filename, image = get_image(url, use_webp)
        if image is None:
            content = error_string("404 Not Found")
            send_request(self, 404, bytes(content, encoding="utf-8"), len(content))
            return
        send_request(self, 200, image, len(image),filename=os.path.basename(filename))

def INT_handler(signum, frame):
    server.server_close()
    exit(0)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    signal.signal(signal.SIGINT, INT_handler)
    signal.signal(signal.SIGHUP, INT_handler)
    config = {"server":"0.0.0.0","port":8080,"location":"./image"}
    if os.path.exists("./config.json"):
        config = json.loads(read_file("./config.json"))
    server_info = (config["server"], config["port"])
    location = config["location"]
    log("info", 'Serving OneAnime on {0}:{1} '.format(server_info[0], server_info[1]))
    server = ThreadingHTTPServer(server_info, RequestHandler)
    server.serve_forever()


