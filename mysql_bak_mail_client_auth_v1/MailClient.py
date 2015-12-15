#!/usr/bin/env python
#coding: utf-8
__author__ = 'allanche'
import socket
import optparse
import sys
from  lib.record_log import savelog
from lib.etc_conf import Yamlconf
from lib.path_get import Path_change
from lib.Authdeclient import Authdeclient
y = Yamlconf()
ip = y.yaml_read()['server_configure']['ip_address']  # server ip
sock = y.yaml_read()['server_configure']['socket']  # server socket
p = Path_change()
errLog = savelog(p.gain_profilePath()+'/log/db_back_log')

def Client(LIST,ip,sock):
    try:
        messages = ' '.join(LIST)
        print "Connect to the server"
        server_address = (ip,int(sock))        #Create a TCP/IP sock
        socks = []
        socks = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socks.connect(server_address)
    except Exception,e:
        error_info = e
        errLog.error(error_info)
        sys.exit()
    try:
        #Sending message from different sockets
        print "  %s sending %s" % (socks.getpeername(),messages)
        socks.send(messages)
    except Exception,e:
        error_info = e

        errLog.error(error_info)
        sys.exit()

    #Read responses on both sockets
    try:
        data = socks.recv(1024)
        print " %s received %s" % (socks.getpeername(),data)
        if not data:
            print "closing socket ",socks.getpeername()
            socks.close()
    except Exception,e:
        error_info = e
        errLog.error(error_info)
        sys.exit()


def main():
    chan = []
    #usage 定义的是使用方法，%prog 表示脚本本身，version定义的是脚本名字和版本号
    try:
        parse=optparse.OptionParser(usage='"usage:%prog [options] arg1,arg2"',version="%prog 1.2")
        parse.add_option('-n','--name',dest='db_name',action='store',type=str,metavar='db_name',help='db_back_name!!')
        parse.add_option('-i','--info',dest='db_info',action='store',type=str,metavar='db_info',help='db_back_info!!')
        parse.add_option('-e','--end',dest='info_end',action='store',type=str,metavar='info_end',help='db_back_info!!')
        parse.add_option('-d','--date',dest='running_date',action='store',type=str,metavar='running_date',help='date!!')
        parse.add_option('-v','--ip',dest='ip_var',action='store',type=str,metavar='ip_var',help='db_back_ip!!')
        parse.add_option('-t','--type',dest='mail_type',action='store',type=str,metavar='mail_type',help='mail type!!')

#-u,--user 表示一个是短选项 一个是长选项
#dest='user' 将该用户输入的参数保存到变量user中，可以通过options.user方式来获取该值
#type=str，表示这个参数值的类型必须是str字符型，如果是其他类型那么将强制转换为str（可能会报错）
#metavar='user'，当用户查看帮助信息，如果metavar没有设值，那么显示的帮助信息的参数后面默认带上dest所定义的变量名
#help='Enter..',显示的帮助提示信息
#default=3306，表示如果参数后面没有跟值，那么将默认为变量default的值
#也可以这样设置默认值
        options,args=parse.parse_args()
        chan = [options.ip_var,options.db_name,options.db_info,options.running_date,options.info_end,options.mail_type]
#        chan = [options.ip_var,options.db_name,options.db_info,options.running_date,options.info_end]
#           -v2 -n3 -i4 -d5 -e6 -t1
        chan = ''.join(chan)
        auth = Authdeclient()    #加密
        auth.declient = chan
        print auth.declient
        Client(auth.declient,ip,sock)
        del auth.declient

    except Exception,e:
        error_info = e
        errLog.error(str(e))
        sys.exit()

if __name__ == "__main__":
    main()