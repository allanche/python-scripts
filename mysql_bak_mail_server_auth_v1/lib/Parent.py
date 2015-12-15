#!/usr/bin/env python2.7
#: coding=utf-8
__author__ = 'allanche'

import sys
import multiprocessing
import time
from lib.send_mail import Mail_get
from lib.etc_conf import Yamlconf
from  lib.record_log import savelog
from lib.timetoala import getTime
from lib.path_get import Path_change

s = savelog()


class ClockProcess(multiprocessing.Process):
    # 继承multiprocessing类
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval
        p = Path_change()
        self.BASE_DIR = p.gain_profilePath()

    # 在子进程中调用mail模块来运行server端。
    def run(self):
        #        errLog = savelog(self.BASE_DIR+'/log/server')
        yamlload = Yamlconf  # yaml解析模块
        current = getTime()  # 时间类
        currenttime = current.timetoala()  # 获取系统当前时间
        print currenttime
        second = current.socktimeout()  # 时间校准
        mailload = Mail_get(yamlload)  # 邮件构造及发送模块
        tryMail = mailload.try_mail(10)  # 传递超时时间和html的模块
        if tryMail:
            try:
                print tryMail
                tryMail = mailload.mail_html(currenttime)  # html邮件构造方法
                mailload.send_mail("info", tryMail)  # 邮件发送方法
            except Exception, e:
                error_info = e
                s.error("Parent module run:%s" % error_info)
                sys.exit()
        else:
            sys.exit()


def main():
    while True:
        p = ClockProcess(1)
        p.daemon = True  # 父进程退出子进程也退出
        p.start()
        while True:
            p.join()  # 父进程运行
            print 'ok'
            break


if __name__ == '__main__':
    main()
