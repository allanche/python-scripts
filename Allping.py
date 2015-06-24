#!/usr/bin/env python\
'''
ping server.
'''
import os
import re
import  time
import sys
from  threading import Thread
import string
class testit(Thread):
        def __init__(self,ip):
                Thread.__init__(self)
                self.ip = ip
                self.status = 0
                self.itimezone = [0,0,0,0]
                self.acount =[]
        def run(self):
                pingaling = os.popen("ping -q -c4 "+self.ip,"r")
                while 1:
                        line = pingaling.readline()
                        if not line: break
                        igot = re.findall(testit.lifeline,line)
                        itime = re.findall(testit.timezone,line)
                        if itime:
                                itime = itime[0].replace('/',' ').split(' ')
                                self.itimezone = itime
                        if igot and int(igot[0]) != 0:
                                self.status = int(igot[0])

if __name__ == '__main__':
        testit.lifeline = re.compile(r"([0-9]+)% packet loss")
        testit.timezone = re.compile(r"rtt min/avg/max/mdev = ([0-9./]+) ms")
        print time.ctime()
        pinglist = []
        f = open('ip.txt')
        print '\t\t\t\t\t\trrt'
        print '\tip\tpacket_loss\tmin\tmax\tavg\tmdev'
        for ip in f:
                ip = ip.strip()
                current = testit(ip)
                pinglist.append(current)
                current.start()
        for pingle in pinglist:
                pingle.join()
                print "%s\t\t%s\t%s\t%s\t%s\t%s" % (pingle.ip,pingle.status,pingle.itimezone[0],pingle.itimezone[1],pingle.itimezone[2],pingle.itimezone[3])
        print time.ctime()
