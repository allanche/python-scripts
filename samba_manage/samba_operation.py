#coding: utf-8
import re
import yaml
import os
from random import choice
import string
import pexpect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from string import Template
import time
from lib.record_log import Logger,log_record
from lib.path_get import gain_profilePath
from lib.admin_conf import userconf
#正则name.yaml配置文件的匹配规则
ru = re.compile(r'''
    \s+
    \s+
    passwd:
    \s+
    (none)
        ''',re.VERBOSE)



#生成随机密码
def GenPasswd(length=8,chars=string.letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

#判断是否为add操作然后生成随机密码
def pass_count():  
    count = 0
    list_pass = []
    di = yaml.load(file(gain_profilePath('/etc/name.yaml'), 'r'))
    for i in di.items():
        if i[1]['op'] == 'add':
            count += 1
    for i in range(count):
        trunk_pass = GenPasswd(12)
        list_pass.append(trunk_pass)
    return list_pass

#替换旧的配置文件，写入内容保存
def add_pass(x):
    old_file = gain_profilePath('/etc/name.yaml')
    f = open(old_file,'r')
    for_pass = []
    w_str=""
    if x is None:
        exit(0)
    else:
        for line in f:
            if ru.search(line):
                line = ru.sub('  passwd: '+''.join(x[:1]),line)
                x = x[1:]
                w_str+=line
            else:
                w_str+=line
        wf = open(old_file,'w')
        wf.write(w_str)
        f.close()
        wf.close()

#账号添加操作
def add_account(i,x,y):
    if i[1]['op'] == 'add':
        try:
            os.system('useradd  -s /sbin/nologin '+i[1]['username'])
        except Exception,e:
            error_info = i[1]['username'] + " Account add exception\n"
            log_record(error_info)
            exit(0)
        print i[1]['passwd']
        child = pexpect.spawn (x)
        child.expect ('New SMB password:')         
        child.sendline(y)                   
        child.expect('Retype new SMB password:')   
        child.sendline(y)
        return child
        debug_info = i[1]['username']+" add success"
        log_record(debug_info)
#账号权限修改操作
def add_mod_dir_auth(i):

    if i[1]['op'] != 'del':
 #       try:
        for n in i[1]['dir'].items():
            try:
                os.path.isdir(n[0])
                facl_fir = 'setfacl -d  -R -m user:'+i[1]['username']+':'+n[1]+' '+n[0]
                facl_sec = 'setfacl  -R -m user:'+i[1]['username']+':'+n[1]+' '+n[0]
            except Exception,e:
                error_info = n[0]+" dir is not exists!\n"
                log_record(error_info)
                exit(0)
  #      except Exception,e:
  #         log_record(e)
  #          exit(0)
        try:
            os.system(facl_fir.encode("utf8"))
            os.system(facl_sec.encode("utf8"))
        except Exception,e:
            error_info = i[1]['username']+facl_fir+" Add permissions abnormal!\n"
            log_record(error_info)
            exit(0)
#删除操作
def del_account(i):
   
    if i[1]['op'] == 'del':
        try:
            os.system('userdel '+i[1]['username'])
        except Exception,e:
            error_info = i[1]['username']+" Delete accounts abnormal! \n"
            log_record(error_info)
            exit(0)
    
#邮件内容模板函数
def SEND_MAIL(k,sender,password):
    '''
    send mail
    '''
    subject = 'python email test'
    smtpserver = 'smtp.163.com'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = u"共享文件服务器" 
    company_name = k[0].split('_')[0]
    user = k[1]['username']
    Pass = k[1]['passwd']
    if 'vpn' in k[1]:
        html = u"""\
            您好，给你新开的VPN账号和密码为：$user,$vpn_pass。VPN连接方法见附件，不会连接VPN的联系网管设定使用。
            您需要的文件系统账号跟密码为：$user，$Pass。
            文件系统使用方法：使用前必须连接上VPN，打开计算机在地址栏输入\\192.168.1.240,然后进入$company_name目录。
            以后文件系统的权限修改请联系yy@xx.com！
            xxx-xxx
        """ 
        html = Template(html)
        if 'vpn' in k[1]:
            html = html.substitute(user=k[1]['username'],Pass=k[1]['passwd'],vpn_pass=k[1]['vpn']['vpn_pass'],company_name=k[0].split('_')[0])
        try:

            attach_file = gain_profilePath('/mail attachment')+userconf()['file name']
            att = MIMEText(open(attach_file, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="file"'
            msg.attach(att)
            part2 = MIMEText(html, 'html','utf-8') 
            msg.attach(part2)
        except Exception,e:
            error_info = e
            log_record(error_info)
            exit(0)
    elif 'mod' in k[1]:
        html = u"""\
            您好，你的文件共享权限已经修改好，
            文件系统使用方法：打开计算机在地址栏输入\\192.168.1.240，进入$company_name目录。
            以后文件系统的权限修改及故障请联系xxx@xxx.com！
            xxx-xxx
        """
        html = Template(html)
        html = html.substitute(company_name=k[0])
        msg = MIMEText(html,'text','utf-8')
    else:
        html = u"""\
            您好，给你新开的文件系统账号和密码为：$user  ,$Pass。
            文件系统使用方法：打开计算机在地址栏输入\\192.168.1.240，进入$company_name目录。
            以后文件系统的权限修改请联系xxx@xxx.com！
            xxx-xxx
        """
        html = Template(html)
        html = html.substitute(user=k[1]['username'],Pass=k[1]['passwd'],company_name=k[0])
        msg = MIMEText(html,'text','utf-8')
#构造附件
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        smtp.login(sender, password)
        smtp.sendmail(sender, k[1]['user_mail'], msg.as_string())
        smtp.quit()
    except Exception,e:
        error_info = e
        log_record(error_info)
        exit(0)
        
#yaml解析
def YAML_RECO():
    '''
    load yaml doc
    '''
    try:
        config = yaml.load(file(gain_profilePath('/etc/name.yaml'), 'r'))
        return config
        log_record("name.yaml open success!")
    except Exception,e:
        error_info = e
        log_record(error_info)
        exit(0)

#记录所有name.yaml里的配置
def save_yaml():
    saveall = gain_profilePath('/save_all_operation/')
    if os.path.exists(saveall) is False:
        os.mkdir(saveall)
    saveallyaml = saveall+'/all_name.yaml'
    f1 = open(gain_profilePath('/etc/name.yaml'),'r')
    f2 = open(saveallyaml ,'a')
    for i in f1.readlines():
        f2.write(i)
    f2.close()
    f1.close()

if __name__ == '__main__':
    address = userconf()['mail']
    p=re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
    match = p.match(address)  
    if match:
        try:
            pas = userconf()['password']
        except Exception,e:
            error_info = e
            log_record(error_info)
            exit(0)
        try:
            pass_count()
        except Exception,e:
            error_info = e
            log_record(error_info)
            exit(0)
        try:
            x = pass_count()
            add_pass(x)
        except Exception,e:
            error_info = e
            log_record(error_info)
            exit(0)
        try:
            con = YAML_RECO()
        except Exception,e:
            error_info = e
            log_record(error_info)
            exit(0)
        try:
            for i in con.items():
                time.sleep(1)
                if i[1]['op'] == 'add':
                    x = 'smbpasswd -a '+i[1]['username']
                    y = i[1]['passwd']
                    child = add_account(i,x,y)
                    child.expect(pexpect.EOF)
                if 'dir' in i[1]:
                    add_mod_dir_auth(i)
                if 'user_mail' in i[1] and add_mod_dir_auth is True:
                    SEND_MAIL(i,address,pas)
                del_account(i)
        except Exception,e:
            error_info = e
            log_record(error_info)
            exit(0)
        save_yaml()
    else:
        log_record('send mail address is error!')
        



