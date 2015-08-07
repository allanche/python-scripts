###DOC:

* mail attachment此目录下要发送附件的话必须要有附件(暂时没有上传附件上来)，配置附件名在userconf.yaml文件里
* etc此目录下要有name.yaml账号信息文件
* samba账号分配地点有三处：a.xx本部（不需要VPN）b.yy（需要VPN） c.外地(VPN)
* 很重要!!!yaml书写规则(严格要求两个空格,二级项前面两个空格,:后面两个空格)：
(需要vpn且添加账号的书写形式)

    name.yaml
	companyname_area:                     此处为对应的一级目录名
    op: add                              此处为对账号执行的操作：1.添加-add,2.删除-del，3.修改-mod
    username: yz                         账号名
    passwd: none                         密码项，只有添加账号需要此项，删除和修改不需要可删除此项
    dir:                                 目录项，dir不可改
      /xxx: r-x                       设置二级目录权限，一级目录也需要设置权限
      /fex/cai: rwx
    user_mail: xxyy@mail.com   对方的邮箱
    vpn:                                 VPN项
      vpn_account: 1234                  账号
      vpn_pass: axax                     密码
    companyname_area:                      删除操作
    op: del
    username: hy
    companyname_area:                      修改操作
    op: mod
    username: chen
    dir:
      /feiyin: r-x
      /feiyin/cai: rwx
    user_mail: chen@xx.com

	userconf.yaml
	mail: 
	password: 
	file name:                     注意空格


* 密码无需手动生成，脚本里有函数生成然后写入name.yaml里，添加账号时你只需在add操作项里添加  passwd: none这么写即可。
* 发送邮箱填写在etc/userconf.yaml配置文件中，自行修改为自己邮箱和密码,还有邮件模板内容里的联系邮箱
