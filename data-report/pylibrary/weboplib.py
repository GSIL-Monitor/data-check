#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from cfg import *
import time

class WebOpLib :
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    wd = webdriver.Chrome(chrome_options=option)
    def __init__(self):
        pass

    def open_browser(self):   #open browser

        self.wd.maximize_window()
        self.wd.implicitly_wait(10)

    def close_browser(self):   #close browser
        self.wd.quit()

    def login(self,vcc_code,username,password):          # login
        self.wd.get(test_login_url)
        self.wd.find_element_by_id("vcc_code").send_keys(vcc_code)
        self.wd.find_element_by_id("username").send_keys(username)
        self.wd.find_element_by_id("password").send_keys(password)
        self.wd.find_element_by_id('btn').click()
        time.sleep(1)

    # def get_listReportTemplate(self):   #进入模板列表页面，获取名字
    #     self.wd.find_element_by_css_selector('ul.nav-list .hsub:nth-child(5)').click()
    #     self.wd.find_element_by_css_selector('li.open>ul>li:nth-child(1)').click()
    #     self.wd.find_element_by_css_selector('li.open>ul>li:nth-child(1) li:nth-child(1)').click()
    #     time.sleep(1)
    #     self.wd.switch_to.frame('frame122')
    #     # tbody=self.wd.find_element_by_css_selector('tbody.ant-table-tbody')
    #     names=self.wd.find_elements_by_css_selector('tbody.ant-table-tbody td:nth-of-type(3)')
    #     typename=self.wd.find_elements_by_css_selector('tbody.ant-table-tbody td:nth-of-type(4)')
    #     roles=self.wd.find_elements_by_css_selector('tbody.ant-table-tbody td:nth-of-type(5)')
    #     status=self.wd.find_elements_by_css_selector('tbody.ant-table-tbody td:nth-of-type(6)')
    #     beizhu=self.wd.find_elements_by_css_selector('tbody.ant-table-tbody td:nth-of-type(7)')
    #     name=[]
    #     for i  in names :
    #         name.append(i.text)
    #     return name
    #
    # def addReportTemplate(self,name,target,roles='None',content='None'):    #新增模板
    #     self.wd.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/a/button').click()
    #
    #     self.wd.find_element_by_css_selector('input[placeholder="请输入模板名称"]').send_keys(name)
    #     self.wd.find_element_by_css_selector('input.ant-radio-input[value="1"]').click()  #启用
    #     self.wd.find_element_by_css_selector('input.ant-radio-input[value="agId"]').click()  #坐席
    #
    #     if  roles!='None':
    #         self.wd.find_element_by_css_selector(
    #             '#root div.add-template-col-wrap>div .ant-select-selection').click()  # 点击可见范围
    #         self.wd.find_element_by_css_selector('li[filename="%s"]' % roles).click()  # 选择可见范围角色
    #     if  content!='None':
    #         self.wd.find_element_by_css_selector('textarea[placeholder="请输入模板描述内容"]').send_keys(content)
    #     self.wd.find_element_by_css_selector('ul.ant-transfer-list-content li[title="%s"] .ant-checkbox'%target).click()
    #     self.wd.find_element_by_xpath('//*[@id="root"]/div/div[11]/div[2]/div/div[2]/button[2]').click()
    #     self.wd.find_element_by_css_selector('button[type="submit"]').click()

if __name__ == '__main__':
    t1=WebOpLib()
    t1.open_browser()
    t1.login(4216082301,2001,123456)
    t1.close_browser()