#!/usr/bin/python3

#written by xpocsn00

import socket
import sys
import re

HOST = '127.0.0.1'
#PORT = 64569 #should been readed from arguments
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    exit(1)

#Returns None if addr does not match
def check_ipv4(addr):
    return re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", addr)

def parse(line):
    check = line.split()

    if(check[0] == "GET"):
        return do_get(line.split('\r\n')[0].split())
    elif(check[0] == "POST"):
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
    if(typ == "A" and not check_ipv4(name)):
        try:
            respond = 'HTTP/1.1 200 OK\r\n\r\n'
            return respond + '{}:{}={}'.format(name, typ, socket.getaddrinfo(name, 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP)[0][4][0] + '\r\n')
        except:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    elif(typ == "PTR" and check_ipv4(name)):
        try:
            respond = 'HTTP/1.1 200 OK\r\n\r\n'
            return respond + '{}:{}={}'.format(name, typ, socket.getnameinfo((name, 80),socket.NI_NAMEREQD)[0] + '\r\n')
        except:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

def do_post(line):
    #control lexical
    check = line.split()
    if(check[0] != "POST" and check[1] != "/dns-query" and check[2] != "HTTP/1.1"):
        return "HTTP/1.1 400 Bad Request\r\n\r\n"
    #separating the header and the data
    line = line.split('\r\n\r\n')
    respond = []

    #generate the data
    for s in line[1].split('\n'):
        s = s.split(':')
        try:
            if(s[1] == 'A'):
                respond.append('{}:{}={}'.format(s[0], s[1], socket.getaddrinfo(s[0], 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP)[0][4][0] + '\r\n'))
            elif(s[1] == 'PTR'):
                respond.append('{}:{}={}'.format(s[0], s[1], socket.getnameinfo((s[0], 80),socket.NI_NAMEREQD)[0] + '\r\n'))
        except:
            continue
    #putting header before the data
    #after clarification edit below
    if(len(respond) == 0):
        return "HTTP/1.1 400 Bad Request\r\n\r\n"
    else:
        out = "HTTP/1.1 200 OK\r\n\r\n"
        for s in respond:
            out += s
        return out

#-------- main body of the program ----------
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST,PORT))
    soc.listen()
    while True:
        conn = None
        try:
            conn, addr = soc.accept()
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.send(parse(data.decode('ascii').strip()).encode('ascii'))
                conn.close()
                break
        except KeyboardInterrupt:
            if conn:
                conn.close()
            break
