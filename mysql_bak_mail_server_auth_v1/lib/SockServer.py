#!/usr/bin/env python2.7
#:coding=utf-8
__author__ = 'allanche'
import select
import socket
import Queue
import sys
import time
from time import strftime, localtime
from lib.record_log import savelog
#from lib.Authdeserver import Authdeserver
from lib.path_get import Path_change

reload(sys)
sys.setdefaultencoding("utf-8")  # windows默认采用gbk编码，而在python中字符串都是采用utf8编码，所以这里我们要设置系统编码先为
# utf8，然后对接受的内容进行decode为gbk编码,在解码为utf8，由一种编码到另一种编码，要先decode成对应的编码，
# 在encode到相应的编码。

sa = savelog()


def SockServer(n, ip, sock):
    try:
        #        hostname = socket.gethostname()
        #        ip = socket.gethostbyname(hostname)
        # create a socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        # set option reused
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (ip, int(sock))
        server.bind(server_address)
        server.listen(30)
    except Exception, e:
        error_info = e
        sa.error("SockServer module: %s" % error_info)
        sys.exit()


    # sockets from which we except to read
    # sockets from which we expect to write
    outputs = []
    # Outgoing message queues (socket:Queue)
    message_queues = {}
    timeout = n
    list_data = []

    inputs = [server]
    errLog = savelog()
    while inputs:
        print "waiting for next event"
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
        current = strftime("%H:%M:%S", time.localtime())
        # When timeout reached , select return three empty lists
        if not (readable or writable or exceptional):
            print "Time out ! "
            break
        for s in readable:
            if s is server:
                # A "readable" socket is ready to accept a connection
                connection, client_address = s.accept()
                print "    connection from ", client_address
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
            else:
                data = s.recv(1024)

                if data:
                    print " received ", data.decode('GBK').encode('utf8'), "from ", s.getpeername()
                    sa.info("received from %s %s" % (str(data), str(s.getpeername())))
                    data = data.decode('GBK').encode('utf8')
                    list_data.append(data)
                    message_queues[s].put(data)
                    # Add output channel for response
                    if s not in outputs:
                        outputs.append(s)
                    break


                else:
                    # Interpret empty result as closed connection
                    print "  closing", client_address
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    # remove message queue
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                outputs.remove(s)
            else:
                print " sending ", next_msg.decode('utf8').encode('GBK'), " to ", s.getpeername()
                s.send(next_msg)

        for s in exceptional:
            print " exception condition on ", s.getpeername()
            # stop listening for input on the connection
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            # Remove message queue
            del message_queues[s]
        print current
    print list_data
    return list_data


if __name__ == '__main__':
    SockServer()
