#!/usr/bin/env python2.7
#: coding=utf-8
__author__ = 'allanche'
import time
from time import strftime, localtime
import sys
import time
import datetime
from  lib.record_log import savelog
from lib.path_get import Path_change

s = savelog()


class getTime:
    def __init__(self):
        self.current = ''
        self.subTime = 0
        p = Path_change()
        self.BASE_DIR = p.gain_profilePath()

    # 获取系统当前时间
    def timetoala(self):
        self.current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.current

    # 时间校准器，保证server每天9点都能对收集来的邮件信息进行归档
    def socktimeout(self):
        #        errLog = savelog(self.BASE_DIR+'/log/server')
        try:
            now_gerui = time.mktime(time.localtime())  # 获取现在的格林尼治时间
            future_time = datetime.timedelta(days=1) + datetime.datetime.now()  # 获取now距离将来一天后的事件
            future_gerui = future_time.strftime("%Y-%m-%d %H:%M:%S")  # 对时间进行格式化

            dd = future_time.strftime("%Y-%m-%d") + " 09:00:00"
            future_nine = time.mktime(time.strptime(dd, "%Y-%m-%d %H:%M:%S"))
            future_gerui = time.mktime(time.strptime(future_gerui, "%Y-%m-%d %H:%M:%S"))
            self.subTime = future_gerui - now_gerui
            self.subTimenine = future_nine - now_gerui
            if self.subTimenine != 86400.00:
                return self.subTimenine
            else:
                return self.subTime
        except Exception, e:
            error_info = e
            s.error("timetoala module socktimeout: %s" % error_info)
            sys.exit()


if __name__ == '__main__':
    t = getTime()
    print t.socktimeout()
    currenttime = t.timetoala()  # 获取系统当前时间
    print currenttime
