import cgi
import time
import string
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn

hostIP = ''
portNum = 8080


class mySoapServer(BaseHTTPRequestHandler):
    requests_queue = []      # 任务队列
    captcha_queue = {}       # 验证码值字典，字典每个键代表一个网站，键值是对应网站验证码列表
    captcha_valid_letter = []
    for i in string.digits:
        captcha_valid_letter.append(i)
    for i in string.ascii_letters:
        captcha_valid_letter.append(i)
    captcha_valid_letter.append('-')
    captcha_valid_letter.append('_')
    def do_head(self):
        pass

    def do_GET(self):
        """
        get请求，url分类：
            1、"/" 获取输入验证码任务
                当len(requests_queue)>0时，表示有任务，从requests_queue弹出第0个位置的值返回到前端，进行获取验证码操作
                当len(requests_queue)=0时，表示当前没有任务
        """
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
    <script type="text/javascript">
    </script>
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
                    res = '''<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function Refresh(){
            window.location.reload();
        }
        setTimeout('Refresh()',10000);
    </script>
</head>
<body>
    当前没有请求
</body>
</html>
                    '''
                self.wfile.write(res.encode(encoding='utf_8', errors='strict'))
        except IOError:
            self.send_error(404, message=None)

    def do_POST(self):
        """
        post请求，url分类：
            1、"/" 提交网页上获取的验证码到后台
                captcha_queue字典的键是对应网址，值是对应网址取得的验证码的列表。post提交的值经过校验，添加进captcha_queue字典对应键列表
                TODO
                前端自动将隐藏的值取出，前端检测是否有值，自动提交
            2、"/get_captcha" 请求验证码，并传入任务验证码url。
                在requests_queue列表末尾append新任务，
                看captcha_queue字典键中是否包含新任务的网址，->
                    如果没有，在captcha_queue中增加对应键名，
                    如果有，检查captcha_queue中对应键名的键值（即验证码）是否为空，->
                        如果不为空，直接从captcha_queue中对应键名的键值弹出一个值返回
                        如果为空，则等待15s，15s后再检查captcha_queue中对应键名的键值，->
                            再检查如果为空，返回CAPCHA_NOT_READY
                            再检查如果不为空，从captcha_queue中对应键名的键值弹出一个值返回
        """
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
                captcha_value = form.getvalue('google_captcha')

                # 校验验证码格式，防止恶意提交
                k = 0
                if len(captcha_value) == 420:
                    for i in captcha_value:
                        if i not in self.captcha_valid_letter:
                            break
                        k = k + 1
                    if k == 420:
                        self.captcha_queue[form.getvalue('page_url')].append(captcha_value)


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
                    res = '''<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function Refresh(){
            window.location.reload();
        }
        setTimeout('Refresh()',10000);
    </script>
</head>
<body>
    当前没有请求
</body>
</html>
                    '''
                self.wfile.write(res.encode(encoding='utf_8', errors='strict'))
            elif self.path.split("?")[0] == "/get_captcha":
                #取出请求中的链接添加到requests_queue中，同时前端返回验证码后在字典中生成对应键名的列表
                #给请求传值时剔除字典中对应键名的列表中的对应元素
                #这边post一个链接过来，同时15s内要返回一个google验证码，否则返回空

                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': self.headers['Content-Type'],
                    }
                )
                url = form.getvalue('page_url')
                print(url)

                self.send_response(200, message=None)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                self.requests_queue.append(url)
                if url not in self.captcha_queue:
                    self.captcha_queue[url] = []
                else:
                    if len(self.captcha_queue[url]) != 0:
                        captcha = self.captcha_queue[url].pop()
                        self.wfile.write(captcha.encode(encoding='utf_8', errors='strict'))

                time.sleep(15)

                if len(self.captcha_queue[url]) > 0:
                    print(111)
                    captcha = self.captcha_queue[url].pop()
                    self.wfile.write(captcha.encode(encoding='utf_8', errors='strict'))
                elif len(self.captcha_queue[url]) == 0:
                    print(222)
                    captcha = "CAPCHA_NOT_READY"
                    self.wfile.write(captcha.encode(encoding='utf_8', errors='strict'))
        except IOError:
            self.send_error(404, message=None)


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass


myServer = ThreadingHttpServer((hostIP, portNum), mySoapServer)
myServer.serve_forever()
myServer.server_close()
