import base64
from function import *


def parse(header):
    B = header.split()
    length = len(B)
    method = 0
    url = 0
    payload = 0
    http_version = 0
    if length > 1:
        method = B.pop(0)
    if length > 2:
        url = B.pop(0)
    if length > 3:
        http_version = B.pop(0)
    if length > 4:
        B.pop(0)
        payload = " ".join(B)
    return method, url, http_version, payload


class ClientThread:
    def __init__(self):
        print()

    def run(self):
        while True:
            found = 1
            try:
                data = receive()

            except socket.timeout:
                print("Server timed out")
                break
            data = data.decode()
            if not data:
                print("No data received")
                break
            method, url, http_version, payload = parse(data.rstrip())
            http_response = ""
            if method == "POST":
                http_response = http_version + " 200 OK\r\n\r\n"
                f = open("http_response", "wb+")
                f.write(http_response.encode('UTF-8'))
                f.close()
                send("http_response")
                filename1 = url.split(".")
                if filename1[1] == "png":
                    payload = payload[1:].encode("utf-8")
                    payload = base64.b64decode(payload)
                    with open(url, 'wb') as f:
                        f.write(payload)
                else:
                    with open(url, 'wb') as f:
                        f.write(payload.encode('utf-8'))

            elif method == "GET":
                try:
                    file = open(url, "rb")
                except OSError:
                    found = 0

                if found:
                    http_response = http_version + " 200 OK\r\n\r\n"
                    file = file.read()
                    http_response = http_response.encode()
                    http_response = http_response + file
                    f = open("http_response", "wb+")
                    f.write(http_response)
                    f.close()
                    send("http_response")
                # print("Connection ended")
                else:
                    http_response = http_version + " 404 Not Found\r\n\r\n"
                    f = open("http_response", "wb+")
                    f.write(http_response.encode('UTF-8'))
                    f.close()
                    send("http_response")

            if http_version == "HTTP/1.1":
                break


print('The server is ready to receive\n')
while True:
    newthread = ClientThread()
    newthread.run()
