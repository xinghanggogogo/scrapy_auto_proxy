# -*- coding: utf-8 -*-
# 采用select模块实现异步的socket通信
# ----------------
# import socket
#
# host='127.0.0.1'
# port=10000
#
# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect((host,port))
# s.send('hello from client')
# s.close()
# ----------------

import socket
import sys

messages = ['This is the message. ',
            'It will be sent ',
            'in parts.'
            ]

server_address = ('localhost', 10000)

# Create a TCP/IP socket
socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM),
         socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         ]

# Connect the socket to the port where the server is listening
print >>sys.stderr, 'c onnecting to %s port %s' % server_address
for s in socks:
    s.connect(server_address)

for message in messages:

    # Send messages on both sockets
    '''
    s.getpeername()
    返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。
    s.getsockname()
    返回套接字自己的地址。通常是一个元组(ipaddr,port)
    '''
    for s in socks:
        print >>sys.stderr, '%s: sending "%s"' % (s.getsockname(), message)
        s.send(message)

    # Read responses on both sockets
    for s in socks:
        # 默认最大文件描述符1024
        data = s.recv(1024)
        print >>sys.stderr, '%s: received "%s"' % (s.getsockname(), data)
        if not data:
            print >>sys.stderr, 'closing socket', s.getsockname()
            s.close()
