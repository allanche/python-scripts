#!/usr/bin/env python2.7
#:coding=utf-8
__author__ = 'allanche'
import yaml
import os
from lib.record_log import savelog
from lib.path_get import Path_change
import sys
class Yamlconf:
    def __init__(self):
        self.p = Path_change()
        self.BASE_DIR = self.p.gain_profilePath()
        self.config = {}
        self.errLog = savelog(self.BASE_DIR+'/log/db_back_log')
    #读取yaml文件进行load
    def yaml_read(self):

        try:
            etc_file = os.path.abspath(self.BASE_DIR +'/etc/name.yaml')   #无论在windows下还是linux下自动转换路径分隔符
            self.config = yaml.load(file(etc_file,'r'))
            return self.config
        except Exception,e:
            error_info = e
            self.errLog.error(error_info)
            sys.exit()

if __name__ == '__main__':
    y = Yamlconf()
    print y.yaml_read()



