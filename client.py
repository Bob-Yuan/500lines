import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",1234))
while True:
    t=input()
    s.send(t.encode('utf8'))   #客户端先发送信息
    if t == "exit":
        break
    t=s.recv(1024).decode("utf8")
    if t == "exit":
        break
    print(t)
s.close()