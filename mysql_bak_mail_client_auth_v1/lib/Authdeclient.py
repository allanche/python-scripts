# -*- coding: utf-8 -*-
__author__ = 'allanche'
from Crypto.Cipher import AES


#加密模块
class Authdeclient(object):

    def __init__(self):
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s : s[0:-ord(s[-1])]
        self.key = '533654d43a8c67af'
        self.sult = None

    @property
    def declient(self):
        return self.sult
    @declient.setter
    def declient(self,text):
        cipher = AES.new(self.key)
        encrypted = cipher.encrypt(self.pad(text)).encode('hex')
        self.sult = encrypted

    @declient.deleter
    def declient(self):
        del self.sult


