#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
'''取token'''

#定义函数
def readTime():#到配置文件读时间等数据
    out = open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\token_conf.txt', encoding='utf-8')
    lines = out.readline()
    if(lines.__contains__("\n")):
        lines = lines.split("\n")[0]
    lines1 = out.readline()
    if(lines1.__contains__("\n")):
        lines1 = lines1.split("\n")[0]
    lines2 = out.readline()
    if(lines2.__contains__("\n")):
        lines2= lines2.split("\n")[0]
    lines3=out.readline()
    if(lines3.__contains__('\n')):
        lines3=lines3.split('\n')[0]
    lines4=out.readline()
    if(lines4.__contains__('\n')):
        lines4=lines4.split('\n')[0]

    out.close()
    return lines,lines1,lines2,lines3,lines4

def writeTime(nowTime,nowmanage_token,nowPHPSESSID,test_manage_token,test_phpsessid):
    '''写入时间到配置文件'''
    out = open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\token_conf.txt', 'w')
    out.writelines(nowTime)
    out.writelines("\n")
    out.writelines(nowmanage_token)  #线上manage_token
    out.writelines("\n")
    out.writelines(nowPHPSESSID)     #线上phpsessid
    out.writelines("\n")
    out.writelines(test_manage_token) #测试test_manage_token
    out.writelines("\n")
    out.writelines(test_phpsessid)    #测试test_phpsessid

    out.close()

def token(vcc_code, username, password):
    '''selenium+chromeheadless获取线上环境Token'''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(m_url)
    driver.find_element_by_id("vcc_code").send_keys(vcc_code)   #登录
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id('btn').click()

    manage_cookie = str(driver.get_cookie('manage_access_token'))
    # print(manage_cookie)
    php_cookie = str(driver.get_cookie('PHPSESSID'))
    # print(php_cookie)
    driver.quit()

    manage_token = manage_cookie.split(':')[-1].replace('\'', '').strip()[:-1]  #获取线上manage_token
    # print(manage_token)
    php_token = php_cookie.split(':')[-1].replace('\'', '').strip()[:-1]      #获取线上phpsessid
    # print(php_token)

    return manage_token, php_token

def test_token(vcc_code, username, password):
    '''selenium+chromeheadless获取测试环境token'''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(test_login_url)
    driver.find_element_by_id("vcc_code").send_keys(vcc_code)
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id('btn').click()

    manage_cookie = str(driver.get_cookie('manage_access_token'))
    # print(manage_cookie)
    php_cookie = str(driver.get_cookie('PHPSESSID'))
    # print(php_cookie)
    driver.quit()
    # return manage_cookie,php_cookie
    manage_token = manage_cookie.split(':')[-1].replace('\'', '').strip()[:-1]   #获取测试test_manage_token
    # print(manage_token)
    php_token = php_cookie.split(':')[-1].replace('\'', '').strip()[:-1]        #获取测试test_phpsessid
    # print(php_token)
    return manage_token, php_token

staging_url = 'http://m.staging.icsoc.net/'   #预发布环境url
test_login_url = 'http://m-test.icsoc.net/'   #测试环境url
m_url = 'http://m.icsoc.net/'                 #线上环境url

day = 0                 #配置文件中的时间
manage_token=''         #配置文件中的线上token（manage——token用来控制自定义报表和监控的token）
PHPSESSID=''            #配置文件中的线上phpsessid（phpsessid用来控制明细报表的token）
test_manage_token=''    #初始写入配置文件的测试环境的token
test_phpsessid=''

lastTime = readTime()[0]   #上次被调用的时间，存在了配置文件里

vcc = ['6018040801','wuhan']
username = ['zhangwenping','8888']
password = '123456'

if(time.strftime("%d")==lastTime):#如果配置文件里的token是今天的值，则无需再调用token（）方法
    # print("token仍可用，无需刷新")
    pass
else:
    #使用具体数据登录获取Token
    day = time.strftime("%d")
    manage_token = token(vcc[0], username[0], password)[0]  # 登录线上企业
    PHPSESSID = token(vcc[0], username[0], password)[1]

    test_manage_token=test_token(vcc[1],username[1],password)[0]   #登录测试环境
    test_phpsessid=test_token(vcc[1],username[1],password)[1]

    writeTime(day,manage_token,PHPSESSID,test_manage_token,test_phpsessid)
    # print("配置文件中的token不是今天的，所以调用token方法取出最新")

manage_token = readTime()[1]  #线上token
PHPSESSID = readTime()[2]     #线上phpsessid

test_manage_token=readTime()[3]  #测试环境token
test_phpsessid=readTime()[4]     #测试环境phpsessid








































# agIds='255849'



# vcc_code='4216082301'
# username='liqiuwen'
# password='123456'
# class Cfg:
#     def __init__(self):
#         pass
#
#     def token(self, vcc_code, username, password):
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         self.driver = webdriver.Chrome(chrome_options=chrome_options)
#         self.driver.get(staging_url)
#         self.driver.find_element_by_id("vcc_code").send_keys(vcc_code)
#         self.driver.find_element_by_id("username").send_keys(username)
#         self.driver.find_element_by_id("password").send_keys(password)
#         self.driver.find_element_by_id('btn').click()
#
#         manage_cookie = str(self.driver.get_cookie('manage_access_token'))
#         # print(manage_cookie)
#         php_cookie = str(self.driver.get_cookie('PHPSESSID'))
#         # print(php_cookie)
#
#         self.driver.quit()
#         # return manage_cookie,php_cookie
#         manage_token = manage_cookie.split(':')[-1].replace('\'', '').strip()[:-1]
#         # print(manage_token)
#         php_token = php_cookie.split(':')[-1].replace('\'', '').strip()[:-1]
#         # print(php_token)
#         return manage_token, php_token
#     def manage_token(self):
#         t1=Cfg().token('4216082301','2001','123456')
#         # print(t1)
#         return t1[0]
#     def php_token(self):
#         t1=Cfg().token('4216082301','2001','123456')
#         # print(t1)
#         return t1[1]

# if __name__ == '__main__':
#     t1=Cfg().token('4216082301','2001','123456')
#     mtoken=t1[0]
#     ptoken=t1[1]
#     print(mtoken)
#     print(ptoken)


