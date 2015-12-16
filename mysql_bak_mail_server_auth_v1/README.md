### DOC v1 ###
* 脚本用途对于生产环境各个分散的mysql服务器上执行的每天备份工作的邮件通知。使用CS模型。
* 使用server程序需要安装django和PyYAML包

    	pip install django==1.6  #针对python2.6版本
		pip install PyYAML
* 也可以采用源码方式安装python2.7

    	wget http://python.org/ftp/python/2.7.4/Python-2.7.4.tgz

		tar xf  Python-2.7.4.tgz
		./configure --prefix=/usr/local/python2.7.4
		make && make install
		cp  /usr/local/python2.7.4/bin/python /usr/bin/python2.7
		使用server端的两个模块在采用python2.6的pip安装后只需要执行：
		ln -s /usr/lib/python2.6/site-packages/django/  /usr/local/python2.7.4/lib/python2.7/site-packages/
		ln -s /usr/lib64/python2.6/site-packages/yaml/  /usr/local/python2.7.4/lib/python2.7/site-packages/
		python2.7就能够使用django1.8了

* timeout设置为1800秒。这样保证一天对客户端发来的邮件信息进行每天归档发送。
* 客户端的程序需要配合客户端主机上计划任务中的备份脚本来获取位置参数。
* 服务端程序的配置在/etc/name.yaml文件里。主要对发送邮箱和接受邮箱的配置。

				sendmail_configure:            #邮件发送配置
				  mail_host: smtp.XXX.com
				  mail_user: username
				  mail_pass: password
				  mail_postfix: XXX.com
				mailto_list:                   #邮件接收者邮箱
				  - xxx@yyy.com
				  - aaa@bbb.com
				encryptpasswd:                 #加解密密码，为16位，24位或者32位都可以
				  - 533654d43a8c67af
				sendmaildate:                  #mysql邮件备份的每日定时发送时间
				  - 17


* 在server端上先进入/data/sh/mysql_bak_mail_server/目录。然后执行nohup python2.7 MailServer.py &,也可以使用screen或者supervisor来管理进程。


### DOC v2 ###

* 这一版主要修改了`lib/send_mail.py`文件和客户端程序，增加了一个位置变量用来传递邮件通知功能选择，不仅仅是mysql备份的集中通知，
	第二版加入磁盘IO错误检测邮件报警，客户端程序配合shell脚本传递参数。
		标志1表示mysql备份邮件通知
		标志2表示磁盘IO error邮件提醒
* 对磁盘监控的邮件报警表现为及时性的，不会在等待某个时刻到来发送邮件。

### DOC v3 ###

* 这一版主要加入AES加密来对，cs间的通信内容进行加密和解密，`lib\Auth[e/d]n[server/client].py`文件就是加解密模块，密码是可配置的。
* 要使用加密功能必须要安装PyCrypto模块。
* 安装方法：

		pip install pycrypto
* 加密密码配置在`lib/Authdeserver.py`或者`lib/Authdeclient.py`中

