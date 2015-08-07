#coding: utf-8
__author__ = 'chenyz'

#获取name.yaml配置文件的位置
import os
def gain_profilePath(path):
    parent_path = os.getcwd()
    child_path = parent_path+path
    return child_path