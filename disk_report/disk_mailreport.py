#!/usr/bin/env python
# -*- coding: utf-8 -*-
#code: chen
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from string import Template
import time
mailto_list=["@163.com"]
mail_host=""  #设置服务器
mail_user="xx"    #用户名
mail_pass=""   #口令
mail_postfix="163.com"  #发件箱的后缀
head_info = "notice!"

def mailtoadmin(to_list,sub,content):
        me="192.168.1.x backup disk report"+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')    
        msg['Subject'] = sub   
        msg['From'] = me  
        msg['To'] = ";".join(to_list)  
        try:  
                s = smtplib.SMTP()  
                s.connect(mail_host)  
                s.login(mail_user,mail_pass) 
                s.sendmail(me, to_list, msg.as_string()) 
                s.close()  
                return True  
        except Exception, e:  
                print str(e)  
                return False  

def Temp(disk_name,disk_used,content_info): #单独构造一个磁盘的信息
        text = u"""\
                192.168.1.x backup disk:$DISK used:$USED% ,$CONTENT_INFO
                """ 
        text = Template(text)
        text = text.substitute(DISK=disk_name,USED=disk_used,CONTENT_INFO=content_info)
        return text
def Tempall(list_info):  #
        textall = u"""\
                $DISK_INFO1
                $DISK_INFO2
                """
        textall = Template(textall)
        textall = textall.substitute(DISK_INFO1=list_info[0],DISK_INFO2=list_info[1])
        return textall
def main():
        list_info = []
        info = re.compile(r"([/a-z1-9]+).*\s([0-9]+)%\s\S+",re.VERBOSE)
        for i in os.popen('df -Th').readlines()[1:]:
                line_info = info.match(i)
                disk_name = line_info.group(1)
                disk_used = int(line_info.group(2))
                if disk_name == "/dev/sdb1" or disk_name == "/dev/sdc1":
                        if disk_used > 90:
                                content_info = "notice!"
                                list_info.append(Temp(disk_name,disk_used,content_info).strip())
                        elif disk_used > 95:
                                content_info = "There is insufficient space on the disk.warnning!"
                                list_info.append(Temp(disk_name,disk_used,content_info).strip())
        if list_info:
                return list_info
                                                            
if __name__ == '__main__':
        list_info = main()
        if list_info:
                mailtoadmin(mailto_list,head_info,Tempall(list_info))