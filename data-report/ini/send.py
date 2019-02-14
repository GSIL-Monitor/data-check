#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
from interface.test_monitor import *
from BeautifulReport import BeautifulReport
import os
import time
from BeautifulReport import BeautifulReport
from interface.monitor_v111 import *

#发送邮件服务器
smtpserver='smtp.exmail.qq.com'
#发送邮箱用户/密码
user='lvjunlin@icsoc.net'
password='b5La7VJRCkQMhsjF'
#发送邮箱
sender='lvjunlin@icsoc.net'
#接收邮箱
receiver='365837434@qq.com'
#发送邮件主题
subject='Python email test'


# def send_mail(file_new):
#     f=open(file_new,'rb')
#     mail_body=f.read()
#     f.close()
#
#     msg=MIMEText(mail_body,'html','utf-8')
#     msg['Subject'] = Header('自动化测试报告','utf-8')
#
#     smtp=smtplib.SMTP()
#     smtp.connect(smtpserver)
#     smtp.login(user, password)
#     smtp.sendmail(sender, receiver, msg.as_string())
#     smtp.quit()
#     print('email has send out')
def send_mail(file_new):

    f=open(file_new,'rb')
    mail_body=f.read()
    att=MIMEText(mail_body,'base64','utf-8')
    att['Content-Type']='application/octet-stream'
    att['Content-Disposition']='attachment ;filename="log.html"'
    msgRoot=MIMEMultipart('related')
    msgRoot['Subject']=subject
    msgRoot.attach(att)

    smtp=smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()
    print('email has send out')


def new_report(testreport):
    lists=os.listdir(testreport)
    lists.sort(key=lambda fn: os.path.getmtime(testreport+"\\"+fn))
    file_new=os.path.join(testreport,lists[-1])
    print(file_new)
    return file_new

# #发送邮件服务器
# smtpserver='smtp.exmail.qq.com'
# #发送邮箱用户/密码
# user='lvjunlin@icsoc.net'
# password='b5La7VJRCkQMhsjF'
# #发送邮箱
# sender='lvjunlin@icsoc.net'
# #接收邮箱
# receiver='365837434@qq.com'
# #发送邮件主题
# subject='Python email test'

# #发送的附件
# sendfile=open('D:\\IC\\other\\Python_code\\manage_unittest\\report\\','rb').read()
#
#
#
# #编写HTML类型邮件正文
# msg=MIMEText('<html><h1>hello</h1></html>','html','utf-8')
# msg['Subject']=Header(subject,'utf-8')

#连接发送邮件
# smtp=smtplib.SMTP()
# smtp.connect(smtpserver)
# smtp.login(user,password)
# smtp.sendmail(sender,receiver,msg.as_string())
# smtp.quit()


if  __name__ == '__main__':
    test_report='D:\\IC\\other\\Python_code\\manage_unittest\\report\\'
    now = time.strftime("%Y-%m-%d %H_%M_%S")

    htmlfile = 'D:\\IC\\other\\Python_code\\manage_unittest\\report\\'

    suite = unittest.TestSuite()
    # for i in Monitor.list1:
    #     suite.addTest(ParametrizedTestCase.parametrize(Monitor, 'test_OnlineReport',param=i))
    for i in Monitor.list1:
        suite.addTest(ParametrizedTestCase.parametrize(Monitor, 'test_QueReport',param=i))
    BeautifulReport(suite).report(filename='测试报告'+now,description='坐席和队列指标测试_企业:4216082301'
                                  ,log_path=htmlfile)

    new_report=new_report(test_report)
    send_mail(new_report)
    # name = 'lily and lucy'
    # print(name.lower())