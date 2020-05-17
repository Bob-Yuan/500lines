import cgi
import time
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from queue import Queue
from socketserver import ThreadingMixIn
import urllib

hostIP = ''
portNum = 8080


class mySoapServer(BaseHTTPRequestHandler):
    q = Queue()
    def do_head(self):
        pass

    def do_GET(self):
        try:
            self.send_response(200, message=None)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            res = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form action="/" method="POST">
    <input type="text">
    <input type="submit">
</form>
</body>
</html>
           '''
            self.wfile.write(res.encode(encoding='utf_8', errors='strict'))
        except IOError:
            self.send_error(404, message=None)

    def do_POST(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )
            print(form)
            content_len = int(self.headers.get('Content-Length'))
            print(content_len)
            post_body = self.rfile.read(1000)
            print(post_body)
            self.send_response(200, message=None)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            res = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form action="/" method="POST">
    <input type="text">
    <input type="submit">
</form>
</body>
</html>
           '''
            self.wfile.write(res.encode(encoding='utf_8', errors='strict'))
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

