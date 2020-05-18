import cgi
import time
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from queue import Queue
from socketserver import ThreadingMixIn
import urllib
import urllib.parse

hostIP = ''
portNum = 8080


class mySoapServer(BaseHTTPRequestHandler):
    requests_queue = []
    captcha_queue = {}
    def do_head(self):
        pass

    def do_GET(self):
        try:
            # 这边区分一下请求链接，分为请求google_key和请求写入google_key页面
            # print("self.headers", self.headers)
            print("self.path", self.path)
            self.send_response(200, message=None)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if self.path == "/":
                if len(self.requests_queue) > 0:
                    url = self.requests_queue.pop(0)
                    res = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<a href="http://'''+url+'''" target="_blank">'''+url+'''</a>
<form action="/" method="POST" name="form1">
    <input type="text" name="google_captcha">
    <input type="hidden" name="page_url" value="'''+url+'''">
    <input type="submit">
</form>
</body>
</html>
               '''
                else:
                    res = "当前没有请求，请过会儿刷新（这边写一个定时刷新的js）"
                self.wfile.write(res.encode(encoding='utf_8', errors='strict'))
            elif self.path == "/google_captcha":
                res = "1234567890"
                self.wfile.write(res.encode(encoding='utf_8', errors='strict'))
        except IOError:
            self.send_error(404, message=None)

    def do_POST(self):
        try:
            if self.path == "/":
                self.send_response(200, message=None)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': self.headers['Content-Type'],
                    }
                )
                self.captcha_queue[form.getvalue('page_url')].append(form.getvalue('google_captcha'))

                if len(self.requests_queue) > 0:
                    url = self.requests_queue.pop(0)
                    # 这边加一个google打码的链接
                    res = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<a href="'''+url+'''">'''+url+'''</a>
<form action="/" method="POST" name="form1">
    <input type="text" name="google_captcha">
    <input type="hidden" name="page_url" value="'''+url+'''">
    <input type="submit">
</form>
</body>
</html>
'''
                else:
                    res = "当前没有请求，请过会儿刷新（这边写一个定时刷新的js）"
                self.wfile.write(res.encode(encoding='utf_8', errors='strict'))
            elif self.path.split("?")[0] == "/get_captcha":
                #取出请求中的链接添加到requests_queue中，同时前端返回验证码后在字典中生成对应键名的列表
                #给请求传值时剔除字典中对应键名的列表中的对应元素
                #这边post一个链接过来，同时15s内要返回一个google验证码，否则返回空

                # 获取post过来的链接
                parsed = urllib.parse.urlparse(self.path)
                url = parsed[4].split('=')[1]
                self.requests_queue.append(url)
                self.captcha_queue[url] = []
                # print(self.requests_queue)
                # print(self.captcha_queue)
                # 返回post请求
                time.sleep(15)
                self.send_response(200, message=None)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                if len(self.captcha_queue[url]) > 0:
                    captcha = self.captcha_queue[url].pop()
                    self.wfile.write(captcha.encode(encoding='utf_8', errors='strict'))
                    print(self.captcha_queue)
                elif len(self.captcha_queue[url]) == 0:
                    print(222)
                    captcha = "CAPTCHA_HAS_NOT_PREPARED"
                    self.wfile.write(captcha.encode(encoding='utf_8', errors='strict'))
        except IOError:
            self.send_error(404, message=None)


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass


myServer = ThreadingHttpServer((hostIP, portNum), mySoapServer)
myServer.serve_forever()
myServer.server_close()


# import os
# from threading import Thread
# import time
#
# port_number = "8000"
#
#
# def run_on(port):
#     os.system("python -m http.server " + port)
#
# if __name__ == "__main__":
#     server = Thread(target=run_on, args=[port_number])
#     #run_on(port_number) #Run in main thread
#     #server.daemon = True # Do not make us wait for you to exit
#     server.start()
#     time.sleep(2) #Wait to start the server first
#
#
# def test():
#     url = "http://localhost:" + port_number
#     print(url + " is opened in browser")
#
#
# test()

