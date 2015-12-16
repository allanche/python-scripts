#!/usr/bin/env python2.7
#: coding=utf-8
__author__ = 'allanche'

import smtplib
from email.mime.text import MIMEText
import sys
from lib.etc_conf import Yamlconf
from lib.SockServer import SockServer
from record_log import savelog
from django.conf import settings

settings.configure()
from django.template import Template, Context
from lib.path_get import Path_change
from lib.timetoala import getTime
import sys
from django.core.wsgi import get_wsgi_application
from lib.SockServer import SockServer

application = get_wsgi_application()
import datetime
import os

from lib.Authdeserver import Authdeserver
from django.template.loader import get_template

sa = savelog()


class Mail_get(Yamlconf, getTime):
    def __init__(self, y):

        """

        :type self: object
        """
        y = Yamlconf()
        self.mailto_list = y.yaml_read()['mailto_list']
        self.mail_host = y.yaml_read()['sendmail_configure']['mail_host']  # 设置服务器
        self.mail_user = y.yaml_read()['sendmail_configure']['mail_user']  # 用户名
        self.mail_pass = y.yaml_read()['sendmail_configure']['mail_pass']  # 口令
        self.mail_postfix = y.yaml_read()['sendmail_configure']['mail_postfix']  # 发件箱的后缀
        self.ip = y.yaml_read()['server_configure']['ip_address']  # server ip
        self.sock = y.yaml_read()['server_configure']['socket']  # server socket
        self.newmail = ''
        self.info = []
        self.endinfo = []
        p = Path_change()
        self.BASE_DIR = p.gain_profilePath()

    # 对构建的邮件进行发送
    def send_mail(self, sub, content):  # to_list：收件人；sub：主题；content：邮件内容
        #        errLog = savelog(self.BASE_DIR+'/log/server')
        me = u"数据库备份通知" + "<" + self.mail_user + "@" + self.mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
        msg = MIMEText(content, _subtype='html', _charset='utf-8')  # 创建一个实例，这里设置为html格式邮件
        msg['Subject'] = sub  # 设置主题
        msg['From'] = me
        msg['To'] = ";".join(self.mailto_list)

        try:
            self.s = smtplib.SMTP()
            self.s.connect(self.mail_host)  # 连接smtp服务器
            self.s.login(self.mail_user, self.mail_pass)  # 登陆服务器
            for i in range(len(self.mailto_list)):
                self.newmail = self.mailto_list[i]
                self.s.sendmail(me, self.newmail, msg.as_string())  # 发送邮件
            self.s.close()
            sa.info("mail send to %s" % self.mailto_list)
            return True
        except Exception, e:
            error_info = e
            sa.error("send_mail module" % error_info)
            sys.exit()

    def mail_html(self, current):  # 利用django template构造邮件html
        #        errLog = savelog(self.BASE_DIR+'/log/server')
        print "mail_html self.endinfo %s" % self.endinfo
        p = Path_change()
        try:


            source_html = u'''
           <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <style type="text/css">
                        h4 {background-color: #E0E0E0}
                        body {background-color: #E0E0E0}
                        p {margin-left: 20px}
                    </style>
                    <title></title>
                </head>
                <body>
                <h4>From:{{ who }}</h3>
                <h4>Date:{{ what }}</h3>

                    {% for name in name_list %}
                        {% if name|last == 'T' %}
                            <p> information: {{ name|cut:"T" }} </p>
                        {% else %}
                            <p style="color:#ff0000">  warnning: {{ name|cut:"F" }} </p>
                        {% endif %}
                    {% endfor %}
                </body>
                </html>

            '''

            # source_html = get_template(p.gain_profilePath()+'/lib/test.html')
            f = Template(source_html)
            function_var = self.endinfo[0].split(' ')[-1]
            mail_var = [' '.join(self.endinfo[0].split(' ')[0:-1])]  # 传进去的是一个['xx']包裹的列表
            print "mail_html function_var:%s" % function_var
            print "mail_html mail_var:%s" % mail_var

            # 通过功能标志来确定邮件标题模板
            if function_var == '1':
                c = Context(
                    {'who': 'database@h4.hadoop',
                     'what': current,
                     'name_list': mail_var
                     }
                )
            elif function_var == '2':
                c = Context(
                    {'who': 'Disk IO ERROR report@h4.hadoop',
                     'what': current,
                     'name_list': mail_var
                     }
                )
            html = f.render(c)
            # html = source_html.render(c)
            return html
        except Exception, e:
            error_info = e
            sa.error("send_mail module mail_html: %s" % error_info)
            sys.exit()

    # 调用SockServer进入sever模式传入超时时间，server进程退出，传递出返回值给html构建模块

    def try_mail(self, subTime):
        self.info = SockServer(subTime, self.ip, self.sock)
        # print "try_mail:%s" % self.info
        if self.info:
            # 数据库备份邮件信息列表构造和时间的约束
            #    print "try_mail:%s" % self.info[0].split(' ')
            # 列表第六个元素为功能标志位,1表示mysql备份邮件通知备份功能

            '''
            数据解密
            '''
            auth = Authdeserver()
            self.info = self.info[0].replace(' ','')
            print "test:%s " % self.info
            auth.deserver = self.info
            self.info = auth.deserver
            del auth.deserver
            self.info = self.info.strip('')
            print "try_mail self.info %s, %s " % (type(self.info),self.info)
            self.info = [self.info.replace('',' ').strip(' ')]
            if self.info[0].split(' ')[-1] == '1':
                try:  # 将sockserver超时返回的值存入邮件文件中
                    #    print 'test:%s ' % self.info
                    writefile = open(self.BASE_DIR + '/lib/maillist', 'a')
                    for writetoline in self.info:
                        writefile.writelines(writetoline + '\n')
                    writefile.close()
                    sa.info("%s:mailist write success!" % self.info)

                    if datetime.datetime.now().hour == 9:  # 判断是否达到发邮件的时间，来读取文件，返回邮件列表
                        if os.path.isfile(self.BASE_DIR + '/lib/maillist'):
                            readfile = open(self.BASE_DIR + '/lib/maillist', 'r')
                            for i in readfile:
                                if i != '\n' or i != '':
                                    type(self.endinfo)
                                    self.endinfo.append(i[0:-1])
                            readfile.close()
                            os.remove(self.BASE_DIR + '/lib/maillist')
                            return self.endinfo
                except Exception, e:
                    error_info = e
                    sa.error("send_mail module try_mail: %s" % error_info)
                    sys.exit()

            # 2表示磁盘IO error检测邮件通知功能
            elif self.info[0].split(' ')[-1] == '2':
                try:
                    if self.info:
                        self.endinfo = self.info
                        #   print 'disk IO error report!'
                        #    print 'try_mail disk:%s' % self.endinfo
                        return self.endinfo
                except Exception, e:
                    error_info = e
                    sa.error("diskreport get the info error: %s" % error_info)
                    sys.exit()


if __name__ == "__main__":
    y = Yamlconf
    m = Mail_get(y)
    t = m.try_mail(10)
    if t:
        mt = m.mail_html()
        m.send_mail("info", mt)
