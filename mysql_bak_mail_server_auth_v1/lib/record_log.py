# coding: utf-8
__author__ = 'allanche'
import logging, logging.handlers
import sys, time, inspect
import os
from lib.path_get import Path_change


# 日志类
class savelog:
    def __init__(self, level="DEBUG"):
        self.LOGFORMAT = "[%(levelname)s] [%(asctime)s] [line:%(lineno)d] %(message)s"
        self.TIMEFORMAT = "%Y-%m-%d"
        self.Date = time.strftime(self.TIMEFORMAT, time.localtime())
        self.Logger = logging.getLogger()
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.handlers = []  # 此处用于初始化hanlders，避免重复写日志
        #        self.add_streamhandler(level)
        self.add_filehandler(level)
        self.LOG_COLORS = {
            'DEBUG': "%s",
            'INFO': "\033[1;32m%s\033[1;0m",
            'WARNING': "\033[1;33m%s\033[1;0m",
            'ERROR': "\033[1;31m%s\033[1;0m",
            'CRITICAL': "\033[1;35m%s\033[1;0m",
        }

    def add_streamhandler(self, method):
        # print self.LOG_COLORS[method.upper()]
        fmt = logging.Formatter(self.LOG_COLORS[method.upper()] % self.LOGFORMAT)
        header = logging.StreamHandler()
        # level = getattr(logging,level.upper(),logging.DEBUG)
        level = getattr(logging, "DEBUG")
        header.setLevel(level)
        header.setFormatter(fmt)
        self.Logger.addHandler(header)
        return header

    def add_filehandler(self, level):
        p = Path_change()
        BASE_DIR = p.gain_profilePath()
        fmt = logging.Formatter(self.LOGFORMAT)
        file = BASE_DIR + '/log/server'
        header = logging.FileHandler(file)
        level = getattr(logging, level.upper(), logging.DEBUG)
        header.setLevel(level)
        header.setFormatter(fmt)
        self.Logger.addHandler(header)

    def debug(self, msg):
        header = self.add_streamhandler("debug")
        self.Logger.debug(msg)
        self.Logger.removeHandler(header)

    def info(self, msg):
        header = self.add_streamhandler("info")
        self.Logger.info(msg)
        self.Logger.removeHandler(header)

    def warning(self, msg):
        header = self.add_streamhandler("warning")
        self.Logger.warning(msg)
        self.Logger.removeHandler(header)

    def error(self, msg):
        header = self.add_streamhandler("error")
        self.Logger.error(msg)
        self.Logger.removeHandler(header)

    def critical(self, msg):
        header = self.add_streamhandler("critical")
        self.Logger.critical(msg)
        self.Logger.removeHandler(header)
