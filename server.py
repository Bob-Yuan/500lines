import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("127.0.0.1",1234))
s.listen(2)
sock,addr=s.accept()
while True:
    t=sock.recv(1024).decode('utf8')   #服务端先接收信息
    if t == "exit":
        break
    print(t)
    t=input()
    if t == "exit":
        break
    sock.send(t.encode('utf8'))
s.close() 