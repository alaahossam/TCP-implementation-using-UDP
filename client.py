import os
from pathlib import Path

import cv2
import base64
from function import *

serverport = 80
serverName = "localhost"
cache = {}
while True:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++Welcome To Network Communication Program+++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("+++++     1- Requesting File Through Web Browser          ++++++++++++++++++++++++++++++")
    print("+++++     2- Sending file Through Local Host              ++++++++++++++++++++++++++++++")
    print("+++++     3- How To use                                   ++++++++++++++++++++++++++++++")
    print("+++++     4- Exit                                         ++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    inp = input("Input>")
    os.system('cls')
    if int(inp) == 2:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++Sending file Through Local Host++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++    1- POST file from client to server          +++++++++++++++++++++++++++++++++++")
        print("+++++    2- GET file from Server                     +++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        inpp = input("Input>")
        os.system('cls')
        if int(inpp) == 1:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("+++++++++++++++++++++++++POST file from client to server++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            inppp = input("Enter file Name>")
            os.system('cls')
            httprequest = ""
            httprequest += "POST "
            httprequest += inppp
            httprequest += " HTTP/1.1\r\nHOST:"
            httprequest += serverName + ":" + str(serverport) + "\r\n\r\n"
            found = 1
            try:
                sentfile = open(inppp, "rb")
            except OSError:
                print("File not found ")
                found = 0
            if found == 1:
                sentfile = sentfile.read()
                filename1 = inppp.split(".")
                httprequest1 = httprequest + "\r\n\r\n"
                if filename1[1] != "png":
                    httprequest = httprequest1 + sentfile.decode('utf-8')
                    f = open("httprequest", "wb+")
                    f.write(bytes(httprequest, 'utf-8'))
                    f.close()
                    send("httprequest")
                    print(httprequest)
                else:
                    sentfile = base64.b64encode(sentfile)
                    httprequest = httprequest1 + str(sentfile)
                    f = open("httprequest", "wb+")
                    f.write(bytes(httprequest, 'utf-8'))
                    f.close()
                    send("httprequest")
                    print(httprequest1)
                print("File sent successfully ")
                data = receive()
                print(data.decode())

        elif int(inpp) == 2:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("+++++++++++++++++++++++++++++GET file from server+++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            inppp = input("Enter file Name>")
            os.system('cls')
            httprequest = ""
            httprequest += "GET "
            httprequest += inppp
            httprequest += " HTTP/1.1\r\nHOST:"
            httprequest += serverName + ":" + str(serverport) + "\r\n\r\n"
            f = open("httprequest", "wb+")
            f.write(bytes(httprequest, 'utf-8'))
            f.close()
            send("httprequest")
            print()
            print("HTTP Request :    ")
            print(httprequest)
            data = receive()
            data = data.split(b"\r\n\r\n")
            response = data[0].decode('UTF-8')
            filename1 = inppp.split(".")
            res = response
            res1 = response.split(" ")
            if res1[1] == "404":
                print(response)
                quit()
            if inppp in cache:
                with open(inppp, 'rb') as f:
                    print("***File found in cache***")
                    if filename1[1] != "png":
                        print(f.read())
                    else:
                        img = cv2.imread(inppp)
                        cv2.imshow('image', img)
                        cv2.waitKey(0)
            else:
                print("***File not found in cache***")
                with open(inppp, 'wb') as f:
                    f.write(data[1])
                    f = open(inppp, 'rb')

                    if filename1[1] != "png":
                        print()
                        print("-----Response Head: ")
                        print(response)
                        print("------Response Data: ")
                        print(data[1].decode())
                    else:
                        img = cv2.imread(inppp)
                        print()
                        print("-----Response Head: ")
                        print(response)
                        print("------Response Data: ")
                        cv2.imshow('image', img)
                        cv2.waitKey(0)
        else:
            print("ENteR tHe RiGhT Choice")
            exit(1)
    elif int(inp) == 1:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        serverPort = 12345
        serverSocket.bind(('127.0.0.1', serverPort))
        print('Ready to serve...')

        file, _ = serverSocket.recvfrom(1024)
        file = file.decode()
        serverSocket.close()
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++Sending file Through Local Host++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++    1- POST file from client to server          +++++++++++++++++++++++++++++++++++")
        print("+++++    2- GET file from Server                     +++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        inpp = input("Input>")
        os.system('cls')
        if int(inpp) == 1:
            inppp = file
            os.system('cls')
            httprequest = ""
            httprequest += "POST "
            httprequest += inppp
            httprequest += " HTTP/1.1\r\nHOST:"
            httprequest += serverName + ":" + str(serverport) + "\r\n\r\n"
            found = 1
            try:
                sentfile = open(inppp, "rb")
            except OSError:
                print("File not found ")
                found = 0
            if found == 1:
                sentfile = sentfile.read()
                filename1 = inppp.split(".")
                httprequest1 = httprequest + "\r\n\r\n"
                if filename1[1] != "png":
                    httprequest = httprequest1 + sentfile.decode('utf-8')
                    f = open("httprequest", "wb+")
                    f.write(bytes(httprequest, 'utf-8'))
                    f.close()
                    send("httprequest")
                    print(httprequest)
                else:
                    sentfile = base64.b64encode(sentfile)
                    httprequest = httprequest1 + str(sentfile)
                    f = open("httprequest", "wb+")
                    f.write(bytes(httprequest, 'utf-8'))
                    f.close()
                    send("httprequest")
                    print(httprequest1)
                print("File sent successfully ")
                data = receive()
                print(data.decode())

        elif int(inpp) == 2:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("+++++++++++++++++++++++++++++GET file from server+++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            inppp = file
            os.system('cls')
            httprequest = ""
            httprequest += "GET "
            httprequest += inppp
            httprequest += " HTTP/1.1\r\nHOST:"
            httprequest += serverName + ":" + str(serverport) + "\r\n\r\n"
            f = open("httprequest", "wb+")
            f.write(bytes(httprequest, 'utf-8'))
            f.close()
            send("httprequest")
            print()
            print("HTTP Request :    ")
            print(httprequest)
            data = receive()
            data = data.split(b"\r\n\r\n")
            response = data[0].decode('UTF-8')
            filename1 = inppp.split(".")
            res = response
            res1 = response.split(" ")
            if res1[1] == "404":
                print(response)
                quit()
            if inppp in cache:
                with open(inppp, 'rb') as f:
                    print("***File found in cache***")
                    if filename1[1] != "png":
                        print(f.read())
                    else:
                        img = cv2.imread(inppp)
                        cv2.imshow('image', img)
                        cv2.waitKey(0)
            else:
                print("***File not found in cache***")
                with open(inppp, 'wb') as f:
                    f.write(data[1])
                    f = open(inppp, 'rb')
                    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    serverPort = 12345
                    serverSocket.bind(('127.0.0.1', serverPort))
                    print('Wait for sending...')
                    serverSocket.sendto(data[1], ('127.0.0.1', 8520))
                    serverSocket.close()
                    if filename1[1] != "png":
                        print()
                        print("-----Response Head: ")
                        print(response)
                        print("------Response Data: ")
                        print(data[1].decode())
                    else:
                        img = cv2.imread(inppp)
                        print()
                        print("-----Response Head: ")
                        print(response)
                        print("------Response Data: ")
                        cv2.imshow('image', img)
                        cv2.waitKey(0)
        else:
            print("ENteR tHe RiGhT Choise")
            exit(1)
    elif int(inp) == 3:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++HOW TO USE THE PROGRAM+++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        text = "HTML file"
        target = str(Path().absolute()) + '\\file.html'
        print(f"+++ 1- Requesting file from the webBrowser make you GET files from \u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\ +++++++++++")
        print("+++--------------------------------------------------------------------------+++++++++++")
        print("+++ open proxy.py in another shell & server.py in other shell ++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++ 2- Sending file through the Local HOST +++++++++++++++++++++++++++++++++++++++++++++")
        print("+++----------------------------------------+++++++++++++++++++++++++++++++++++++++++++++")
        print("+++ You just need to open server.py only +++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print()
        print("1- back                     2- Exit")
        z = input("Input>")
        if int(z) == 1 :
            os.system('cls')
        else:
            break
    elif int(inp) == 4:
        break
    else:
        print("ENteR tHe RiGhT Choise")
        exit(1)


# file = open("client.txt", "r")
# for line in file:
#     words = line.split()
#     print(words)
#     found = 1
#     httprequest = ""
#     if words[0]:
#         method = words[0]
#         httprequest = httprequest + method + " "
#     if words[1]:
#         filename = words[1]
#         httprequest = httprequest + filename + " HTTP/1.1\r\nHOST:"
#     if len(words) == 3:
#         serverName = words[2]
#         httprequest = httprequest + serverName + ":"
#     else:
#         httprequest = httprequest + serverName + ":"
#     if len(words) == 4:
#         serverport = words[3]
#         httprequest = httprequest + str(serverport) + "\r\n\r\n"
#     else:
#         httprequest = httprequest + str(serverport) + "\r\n\r\n"
#
#     # post method
#     if words[0] == "POST":
#         try:
#             sentfile = open(words[1], "rb")
#         except OSError:
#             print("File not found ")
#             found = 0
#         if found == 1:
#             sentfile = sentfile.read()
#             filename1 = filename.split(".")
#             httprequest1 = httprequest + "\r\n\r\n"
#             if filename1[1] != "png":
#                 httprequest = httprequest1 + sentfile.decode('utf-8')
#                 f = open("httprequest", "wb+")
#                 f.write(bytes(httprequest, 'utf-8'))
#                 f.close()
#                 send("httprequest")
#                 print(httprequest)
#             else:
#                 sentfile = base64.b64encode(sentfile)
#                 httprequest = httprequest1 + str(sentfile)
#                 f = open("httprequest", "wb+")
#                 f.write(bytes(httprequest, 'utf-8'))
#                 f.close()
#                 send("httprequest")
#                 print(httprequest1)
#             print("File sent successfully ")
#             data = receive()
#             print(data.decode())
#
#             serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             serverPort = 12345
#             serverSocket.bind(('127.0.0.1', serverPort))
#             print('Wait for sending...')
#             serverSocket.sendto(data , ('127.0.0.1', 8520))
#             serverSocket.close()
#     # get method
#     if words[0] == "GET":
#         f = open("httprequest", "wb+")
#         f.write(bytes(httprequest, 'utf-8'))
#         f.close()
#         send("httprequest")
#         print(httprequest)
#         data = receive()
#         data = data.split(b"\r\n\r\n")
#         response = data[0].decode('UTF-8')
#         filename1 = filename.split(".")
#         res = response
#         res1 = response.split(" ")
#         if res1[1] == "404":
#             print(response)
#             quit()
#         print(response)
#         if filename in cache:
#             with open(filename, 'rb') as f:
#                 print("File found in cache")
#                 if filename1[1] != "png":
#                     print(f.read())
#                 else:
#                     img = cv2.imread(filename)
#                     cv2.imshow('image', img)
#                     cv2.waitKey(0)
#         else:
#             print("File not found in cache")
#             with open(filename, 'wb') as f:
#                 f.write(data[1])
#                 cache.update({filename: filename})
#                 f = open(filename, 'rb')
#
#                 serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#                 serverPort = 12345
#                 serverSocket.bind(('127.0.0.1', serverPort))
#                 print('Wait for sending...')
#                 serverSocket.sendto(data[1], ('127.0.0.1', 8520))
#                 serverSocket.close()
#
#                 if filename1[1] != "png":
#                     print(data[1].decode())
#                 else:
#                     img = cv2.imread(filename)
#                     cv2.imshow('image', img)
#                     cv2.waitKey(0)
