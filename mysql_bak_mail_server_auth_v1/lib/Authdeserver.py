# -*- coding: utf-8 -*-
__author__ = 'allanche'
from Crypto.Cipher import AES

#解密模块

class Authdeserver(object):
    def __init__(self):
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]
        self.key = '533654d43a8c67af'
        self.sult = None

    @property
    def deserver(self):
        return self.sult

    @deserver.setter
    def deserver(self, encrypted):
        cipher = AES.new(self.key)
        decrypted = self.unpad(cipher.decrypt(encrypted.decode('hex')))
        self.sult = decrypted

    @deserver.deleter
    def deserver(self):
        del self.sult
