# -*- coding: utf-8 -*-

class color:
    def __init__(self):
        pass

    def RED(self, char):
        return "\033[1;31m %s \033[1;0m" % char

    def GREEN(self, char):
        return "\033[1;32m %s \033[1;0m" % char

    def YELLOW(self, char):
        return "\033[1;33m %s \033[1;0m" % char

    def BLUE(self, char):
        return "\033[1;34m %s \033[1;0m" % char

    def PURPLE(self, char):
        return "\033[1;35m %s \033[1;0m" % char

    def CYAN(self, char):
        return "\033[1;36m %s \033[1;0m" % char

    def GRAY(self, char):
        return "\033[1;37m %s \033[1;0m" % char

    def WHITE(self, char):
        return "\033[1;38m %s \033[1;0m" % char
