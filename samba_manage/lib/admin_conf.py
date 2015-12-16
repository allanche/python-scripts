__author__ = 'chenyz'
#coding: utf-8
import yaml
from lib.record_log import Logger
from lib.record_log import log_record
from lib.path_get import gain_profilePath
def userconf():
    try:
        config = yaml.load(file(gain_profilePath('/etc/userconf.yaml'), 'r'))
        return config
    except Exception,e:
        error_info = e
        log_record(error_info)
        exit(0)