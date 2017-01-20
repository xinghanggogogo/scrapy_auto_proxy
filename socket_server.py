# -*- coding: utf-8 -*-
# 采用select模块实现异步的socket通信
# ------------------------------
# import socket
# import select
#
# server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# server.bind(('127.0.0.1', 10000))
# server.listen(5)
#
# inputs=[server]
#
# #保持执行
# while 1:
#     rs, ws, es=select.select(inputs, [], [], 1)
#     for r in rs:
#         if r is server:
#             clientsock, clientaddr=r.accept()
#             inputs.append(clientsock)
#         else:
#             data=r.recv(1024)
#             if not data:
#                 inputs.remove(r)
#             else:
#                 print data

# --------------------------------
import select
import socket
import sys
import Queue

# Create a TCP/IP socket
'''
第1步是 创建socket对象。调用socket构造函数。
socket=socket.socket(familly,type)
    family的值可以是AF_UNIX(Unix域，用于同一台机器上的进程间通讯)，也可以是AF_INET（对于IPV4协议的TCP和 UDP），
    至于type参数，SOCK_STREAM（流套接字）或者 SOCK_DGRAM（数据报文套接字）,SOCK_RAW（raw套接字）。
    server.setblocking(0) server.blocking(0)设置为非阻塞模式
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

'''
第2步，则是将socket绑定（指派）到指定地址上并开始监听连接: socket.bind((host,port)),server.listen(5),最大监听数量
'''
# Bind the socket to the port
server_address = ('localhost', 10000)
server.bind(server_address)
print >>sys.stderr, 'starting up on %s port %s' % server_address
server.listen(5)

'''
inputs：从客户端读取(readable)的活跃的socket列表，先默认添加server
outputs：可以写入客户端(writable)的活跃的socket列表
'''
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    print >>sys.stderr, '\nwaiting for the next event'
    timeout = 1
    '''
    第一次循环的时候inputs列表里已经有server.
    select.select（rlist, wlist, xlist[, timeout]） 传递三个参数，一个为输入而观察的文件对象列表，一个为输出而观察的文件对象列表和一个观察错误异常的文件列表。
    第四个是一个可选参数，表示超时秒数。其返回3个tuple，每个tuple都是一个准备好的对象列表，它和前边的参数是一样的顺序。
    '''
    readable,writable,exceptional = select.select(inputs, outputs, inputs, timeout)

    # 处理input监听队列
    # 超时情况
    if not(readable or writable or exceptional):
        print >>sys.stderr, 'timed out , do something else here...'
        continue
    for s in readable:
        '''
        server ready to connect client：准备建立连接--标识：
        readable列表里有 server（因为inputs之前已经有server，如果,循环readable里有server的话，那么说明准备和一个客户端建立连接。）
        '''
        if s is server:
            connection, client_address = s.accept()
            print >>sys.stderr, 'new connection from', client_address
            connection.setblocking(0)  # 设成非阻塞模式：
            inputs.append(connection)  # 把inputs添加这个connection，也就是添加一个活跃可以读取数据的客户端socket。

            # Give the connection a queue for data we want to send
            '''
            把这个socket对象（connection），建一个我们以后可以发送数据的队列（queue）。
            message_queues本是个空字典
            '''
            message_queues[connection] = Queue.Queue()

        # 已经建立连接
        else:
            data = s.recv(1024)
            # 如果从可读取的客户端socket接收到数据的话：
            if data:
                print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                '''
                我们就往队列里放个数据
                message_queues[s].put(data)，#这里的s其实就是情况1准备建立连接的connection。
                情况1的时候，已经建立好队列了。
                '''
                message_queues[s].put(data)
                # 这个s到底是什么呢
                print '######message_queue######'
                print  message_queues
                # Add output channel for response
                # 假如客户端socket不在可输出的列表里，就加入到列表了。
                if s not in outputs:
                    outputs.append(s)

            # data=None 就是这个客户端已经断开了，所以你再通过recv()接收到的数据就为空了，所以这个时候你就可以把这个跟客户端的连接关闭了。
            else:
                # Interpret empty result as closed connection
                print >>sys.stderr, 'closing', client_address, 'after reading no data'
                # Stop listening for input on the connection
                if s in outputs:
                    # 既然客户端都断开了，我就不用再给它返回数据了，所以这时候如果这个客户端的连接对象还在outputs列表中，就把它删掉
                    # 如果存在，就从活跃可写入的socket列表里删除
                    outputs.remove(s)

                print 'wriatable---before::',writable
                if s in writable:
                    writable.remove(s) # 如果存在，就从写入的列表里删除
                inputs.remove(s)       # 活跃可读的socket列表里删除
                s.close()              # 把连接关闭

                # Remove message queue
                del message_queues[s]

    print message_queues
    print 'wriatable:',writable

    # Handle outputs
    '''
    循环处理可写socket列表。
    如果有数据则发送回客户端，如果没数据则就把这个连接从output list中移除，outputs是活跃可写的socket列表。
    这样下一次循环select()调用时检测到outputs list中没有这个连接，那就会认为这个连接还处于非活动状态
    '''
    for s in writable:
        try:
            '''
            q.get([block[, timeout]]) 获取队列，timeout等待时间
            q.get_nowait() 相当q.get(False) 非阻塞
            '''
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:    # 假如队列为空
            # No messages waiting so stop checking for writability.
            print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
            outputs.remove(s)   # 活跃可写socket列表删除此socket。
        else:                   # 假如队列有数据
            # 客户端socket实例.getpeername()获取客户端的ip和端口
            print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
            s.send(next_msg)    # 发送数据

    # 最后，如果在跟某个socket连接通信过程中出了错误，就把这个连接对象在inputs\outputs\message_queue中都删除，再把连接关闭掉。
    # Handle "exceptional conditions"
    for s in exceptional:
        # 客户端socket实例.getpeername()获取客户端的ip和端口
        print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        inputs.remove(s)        # 活跃可读socket列表删除此socket。
        if s in outputs:
            outputs.remove(s)   # 活跃可写socket列表删除此socket。
        s.close()               # 连接关闭

        # Remove message queue
        del message_queues[s]