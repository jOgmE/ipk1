#!/usr/bin/env python3

#written by xpocsn00

import socket

HOST = '127.0.0.1'
PORT = 64568 #should been readed from arguments

def parse(line):
    line = line.strip().split()

    if(line[0] == "GET"):
        return do_get(line)
    elif(line[0] == "POST"):
        return do_post(line)
    else:
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

def do_get(line):
    #controlling requisites
    if(line[2] != "HTTP/1.1"):
        return "HTTP/1.1 400 Bad Request\r\n\r\n"
    #parsing the request
    try:
        operation = line[1].split('?')
        name = operation[1].split("name=")[1]
        typ = name.split("&type=")
        name = typ[0]
        typ = typ[1]
        operation = operation[0]
    except:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    if(operation != "/resolve"):
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    #sending response regard the requested respond
    if(typ == "A"):
        try:
            respond = 'HTTP/1.1 200 OK\r\n\r\n' + name + ':' + typ + '='
            return respond + socket.getaddrinfo(name, 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP)[0][4][0] + '\r\n'
        except:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    elif(typ == "PTR"):
        try:
            respond = 'HTTP/1.1 200 OK\r\n\r\n' + name + ':' + typ + '='
            return respond + socket.getnameinfo((name, 80),socket.NI_NAMEREQD)[0] + '\r\n'
        except:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

#-------- main body of the program ----------
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST,PORT))
    soc.listen()
    while True:
        conn, addr = soc.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(parse(data.decode('ascii').split('\r\n')[0]).encode('ascii'))
            conn.close()
            break
