# coding: utf-8
__author__ = 'allanche'

# 获取name.yaml配置文件的位置
import os
import sys


# from lib.record_log import *
# 获取当前程序包所在的路径
class Path_change:
    def __init__(self):
        self.BASE_DIR = ''

    def gain_profilePath(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return self.BASE_DIR


'''
if __name__ == '__main__':
    gain_profilePath()
'''
