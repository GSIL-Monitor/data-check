#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import threading
import _thread
# from interface.interface_report1 import *
import smtplib,os
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
from BeautifulReport import BeautifulReport
from interface.monitor_v111 import *

# # 把list1分成兩份，開兩個線程，看能不能節省一半時間
# dxclist1 = []  # 多线程list1
# dxclist2 = []  # 多线程list2
# for index in range(len(Monitor.list1)):
#     if index / 2 == 1:
#         dxclist1.append(Monitor.list1[index])
#     else:
#         dxclist2.append(Monitor.list1[index])
#
#
# def paoList(list):
#     for i in list:
#         suite.addTest(ParametrizedTestCase.parametrize(Monitor, 'test_OnlineReport', param=i))  # 测试用例加入到测试套件
#
#
# threads = []
# t1 = threading.Thread(target=paoList,args=(dxclist1))
# threads.append(t1)
# t2 = threading.Thread(target=paoList,args=(dxclist2))
# threads.append(t2)

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

def send_mail(file_new):
    '''发送邮件'''
    f=open(file_new,'rb')
    mail_body=f.read()
    att=MIMEText(mail_body,'base64','utf-8')
    att['Content-Type']='application/octet-stream'
    att['Content-Disposition']='attachment ;filename="CTI_report.html"'  #邮件名
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

if  __name__ == '__main__':

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(InterfaceReport1('test_Agreport1'))
    htmlfile = 'D:\\IC\\other\\Python_code\\CTI_report\\report\\'
    # fp = open(htmlfile, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='测试报告', description='用例执行情况')
    # runner.run(suite)
    # fp.close()
    suite = unittest.TestSuite()   #测试套件
    #suite.addTest(InterfaceReport1('test_Agreport1'))
    # for i in list:
    #     suite.addTest(ParametrizedTestCase.parametrize(InterfaceReport1, 'test_AgReport',param=i))

    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # t.join()#多线程都走完了，再走主线程
    # tiaoguocishu=0
    for i in Monitor.list1:
        # if i[8].strip() not in shouldSkip:
        suite.addTest(ParametrizedTestCase.parametrize(Monitor, 'test_OnlineReport',param=i))#测试用例加入到测试套件
        # else:
        #     tiaoguocishu+=1
        #suite.addTest(ParametrizedTestCase.parametrize(Monitor, 'test_OnlineReport', param=i))  # 测试用例加入到测试套件
    BeautifulReport(suite).report(filename='测试报告'+now,description=vcc[0]+'企业：自定义报表测试-线上与测试环境对比'
                                   ,log_path=htmlfile)
    new_report = new_report(htmlfile)
    send_mail(new_report)

    # print("跳过用例数为："+str(tiaoguocishu))
    if len(listFinal)!=0:
        #生成报告后将finallist写入到csv中
        #先覆盖写第一句话-
        out = open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\test_online_report_data'+vcc[0]+'.csv','w',
                   encoding="utf-8",newline='')
        writer=csv.writer(out)
        firstLine="开始时间","结束时间","自定义报表模板名称","坐席工号","技能组名称","号码组","呼叫中心",\
                  "指标名称(英文)","指标中文名称","线上查询结果","测试环境查询结果","结果"
        writer.writerow(firstLine)
        # for i in range(len(Monitor.list1)):
        #     writer.writerow(Monitor.list1[i])
        out.close()
        #然后追加新list 'a+'
        out = open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\test_online_report_data'+vcc[0]+'.csv','a+',
                   encoding="utf-8",newline='')
        writer=csv.writer(out)
        for i in range(len(listFinal)):
            writer.writerow(listFinal[i])
        out.close()
