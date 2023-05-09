from socket import *
from urllib.parse import unquote
import datetime

serverSocket = socket(AF_INET, SOCK_STREAM)
proxy = socket(AF_INET, SOCK_DGRAM)
serverPort = 5678
serverSocket.bind(('127.0.0.1', serverPort))
proxy.bind(('127.0.0.1', 8520))
serverSocket.listen(5)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print("addr:\n", addr)
    try:
        message = connectionSocket.recv(1024)  # Fill in start #Fill in end
        message = unquote(message.decode())
        print("message: \n", message.encode())

        message = message
        filename = message.split()[1]

        filename = filename[7:]
        print(filename)
        proxy.sendto(filename.encode(), ('127.0.0.1', 12345))
        # f = open(filename[1:])
        # outputdata = f.read()
        # print("outputdata:", outputdata)
        message , _ = proxy.recvfrom(1024)
        message = message.decode()
        print(message)
        now = datetime.datetime.now()

        first_header = "HTTP/1.1 200 OK"

        header_info = {
            "Date": now.strftime("%Y-%m-%d %H:%M"),
            "Content-Length": len(message),
            "Keep-Alive": "timeout=%d,max=%d" % (10, 100),
            "Connection": "keep-alive",
            "Content-Type": "text/html"
        }

        following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
        print("following_header:", following_header)

        connectionSocket.send(b'\nHTTP/1.1 200 OK\n\n')
        for i in range(0, len(message)):
            connectionSocket.send(bytes(message[i], 'utf-8'))
        connectionSocket.close()
    except IOError:
        connectionSocket.send(
            b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>404 Not Found<h1></body></html>")

        connectionSocket.close()

serverSocket.close()


