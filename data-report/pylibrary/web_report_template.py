#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
from pylibrary.weboplib import WebOpLib

class   Custom_reportLib:
    '''selenium实现增删改查模板'''
    def __init__(self):
        self.wd=WebOpLib().wd

    def go_listReportTemplate(self):   #进入模板列表页面
        self.wd.switch_to_default_content()
        time.sleep(0.5)
        # self.wd.find_element_by_css_selector('div.nav-wrap > div > ul > li:nth-child(1) > a').click()  #系统管理
        self.wd.find_element_by_css_selector('div.nav-wrap > div > ul > li:nth-last-child(1) ').click()  #系统管理
        time.sleep(0.3)
        # self.wd.find_element_by_css_selector('div.nav-wrap > div > ul > li:nth-child(1) > ul>:nth-child(1)').click()  #系统管理-角色管理
        # time.sleep(0.5)
        self.wd.find_element_by_css_selector('div > ul > li:nth-child(5)>a').click()  #统计报表
        time.sleep(0.3)
        self.wd.find_element_by_css_selector('div > ul > li:nth-child(5)>ul>:nth-child(1)').click()  #自定义报表
        time.sleep(0.3)
        self.wd.find_element_by_css_selector('div > ul > li:nth-child(5)>ul>:nth-child(1)>ul>:nth-child(1)').click()  #模板管理
        # time.sleep(1)
        self.wd.switch_to.frame('frame120')

    def get_reportTemplate_name(self):   #获取模板列表名称
        # tbody=self.wd.find_element_by_css_selector('tbody.ant-table-tbody')
        while True:
            self.wd.implicitly_wait(1)
            names=self.wd.find_elements_by_css_selector('div.custom-reports-table-wrap div.ant-table-body td:nth-of-type(3)')
            if names == []:
                return 'None'
        # typename=self.wd.find_elements_by_css_selector('div.custom-reports-table-wrap div.ant-table-body  td:nth-of-type(4)')
        # roles=self.wd.find_elements_by_css_selector('div.custom-reports-table-wrap div.ant-table-body  td:nth-of-type(5)')
        # status=self.wd.find_elements_by_css_selector('div.custom-reports-table-wrap div.ant-table-body  td:nth-of-type(5)')
        # beizhu=self.wd.find_elements_by_css_selector('div.custom-reports-table-wrap div.ant-table-body  td:nth-of-type(5)')
            name=[]
            for i  in names :
                name.append(i.text)
            return name
    def addReportTemplate(self,name,data=None,status=None,objtype=None,roles=None,content=None,report_type=None,index=None): #新增模板
        # self.wd.switch_to.frame('frame120')
        self.wd.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/a/button').click()
        time.sleep(0.25)
        # t=int(time.time())      #获取当前时间戳
        self.wd.find_element_by_css_selector('input[placeholder="请输入模板名称"]').send_keys(name)
        if  status !=None:
            if  status =='启用':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="1"]').click()  #状态：启用
            elif    status=='停用':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="0"]').click()  #停用
            else:
                print('%s,无此状态'%(status))
        if objtype !=None:              #对象类型
            if objtype =='坐席':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="agId"]').click()
            elif    objtype=='业务组':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="grpId"]').click()  #
            elif    objtype=='技能组':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="callQue"]').click()
            elif    objtype=='号码组':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="number"]').click()
            elif objtype == '呼叫中心':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="callcenter"]').click()
            else:
                print('%s,无此对象类型'%(objtype))
            # time.sleep(1)

        if roles !=None:
            self.wd.find_element_by_css_selector(
                '#root div.add-template-col-wrap>div .ant-select-selection').click()  # 点击可见范围
            time.sleep(0.25)
            roles1=self.wd.find_elements_by_css_selector('ul[role="listbox"]>li')
            if type(roles) == type('str'):  # 如果传的是单个字符串参数
                for i in range(len(roles1)):
                    if roles == roles1[i].text:
                        roles1[i].click()
                # self.wd.find_element_by_css_selector('div.add-template-col-title').click()   #点击无效区域
            else:
                for i in range(len(roles)):    # 选择可见范围角色
                    for j in range(len(roles1)):
                        if roles[i]==roles1[j].text:
                            roles1[j].click()
            self.wd.find_element_by_css_selector('div.add-template-col-title').click()  # 点击无效区域

        if  content!=None:
            self.wd.find_element_by_css_selector('textarea[placeholder="请输入模板描述内容"]').send_keys(content)


        if  report_type!=None:
            eles = self.wd.find_elements_by_css_selector(
                '.ant-row-flex .ant-checkbox-group span.ant-checkbox')  # 获取所有的报表类型勾选框
            for i in eles:  # 取消勾选所有报表类型
                if 'ant-checkbox-checked' in i.get_attribute('class'):
                    i.click()

            eles1=self.wd.find_elements_by_css_selector('.ant-row-flex .ant-checkbox-group label>span:nth-of-type(2)')#获取所有报表类型名称
            if type(report_type) == type('str'):  # 如果传的是单个字符串参数
                for i in range(len(eles1)):
                    if report_type == eles1[i].text:
                        eles1[i].click()
            else:
                for i in range(len(report_type)): #多选报表类型
                    for j in range(len(eles1)):
                        if report_type[i]==eles1[j].text:
                            eles1[j].click()
        if index  !=None:
            if index == '坐席工作表现报表指标集':
                self.wd.find_element_by_css_selector('div.add-template-col-wrap> button:nth-child(3)').click()
            elif    index == '坐席外呼指标集':
                self.wd.find_element_by_css_selector('div.add-template-col-wrap> button:nth-child(4)').click()
            elif    index =='坐席监控指标集':
                self.wd.find_element_by_css_selector('div.add-template-col-wrap> button:nth-child(5)').click()
            else:
                print('%s,指标集错误'%(index))
        if  data !=None:
            #选择指标
            self.wd.implicitly_wait(1)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=1000")
            time.sleep(0.5)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=2000")
            time.sleep(0.5)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=3000")
            time.sleep(0.5)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=4000")
            time.sleep(0.5)
            self.wd.implicitly_wait(10)
            eles2=self.wd.find_elements_by_css_selector('ul.ant-transfer-list-content>div')  #取到所有个指标
            text=self.wd.find_elements_by_css_selector('ul.ant-transfer-list-content>div span.custom-item')
            checkbox=self.wd.find_elements_by_css_selector('ul.ant-transfer-list-content>div .ant-checkbox')
            # cont=[]
            # for i in text:
            #     cont.append(i.text)
            if   type(data)==type('str'):               #如果传的是单个字符串参数
                for i in range(len(eles2)):
                    if  data==text[i].text:
                        checkbox[i].click()
            else:
                for i in range(len(data)):
                    for j in range(len(eles2)):
                        # if data[i]==eles2[j].find_element_by_css_selector('span.custom-item').text: #判断名称是否相同
                        if data[i]==text[j].text:
                            # if data[i] not in cont[j]:
                            #eles2[j].find_element_by_css_selector('.ant-checkbox').click()     #点击勾选框
                            checkbox[j].click()
                    if  data[i] not in  text:
                        print('%s指标错误' % (data[i]))

        self.wd.find_element_by_css_selector('div.ant-transfer-operation > button:nth-child(2)').click()  #向右
        self.wd.find_element_by_css_selector('button[type="submit"]').click()   #保存模板按钮
        time.sleep(1.5)

    def del_ReportTemplate(self,template_name):  #删除报表模板
        Custom_reportLib().go_listReportTemplate()
        names = self.wd.find_elements_by_css_selector('div.custom-reports-table-wrap div.ant-table-body td:nth-of-type(3)')
        del_button=self.wd.find_elements_by_css_selector('div > i.iconfont.icon-trash')
        for i in range(len(names)):
            if names[i].text == template_name:
                del_button[i].click()
                time.sleep(0.3)
                self.wd.find_element_by_css_selector\
                    ('div.ant-modal-footer >div > button.ant-btn.ant-btn-primary').click()
                # time.sleep(1.5)

    def update_ReportTemplate(self,name,new_name=None,new_status=None,new_objtype=None,new_roles=None,new_content=None,
                              new_report_type=None,new_data=None):                           #编辑报表模板
        # Custom_reportLib().go_listReportTemplate()
        names = self.wd.find_elements_by_css_selector(
            'div.custom-reports-table-wrap div.ant-table-body td:nth-of-type(3)')
        edit_button=self.wd.find_elements_by_css_selector('div > i.iconfont.icon-edit')
        for i in range(len(names)):
            if name == names[i].text:
                edit_button[i].click()   #通过模板报表名称，进入编辑页面
        time.sleep(0.25)
        if new_name!=None:   #修改名称
            self.wd.find_element_by_css_selector('input[placeholder="请输入模板名称"]').clear()
            self.wd.find_element_by_css_selector('input[placeholder="请输入模板名称"]').send_keys(new_name)

        if  new_status!=None:  #修改状态
            if  new_status =='启用':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="1"]').click()  #状态：启用
            elif    new_status=='停用':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="0"]').click()  #停用
            else:
                print('%s,无此状态'%(new_status))

        if new_objtype !=None:              #修改对象类型
            if new_objtype =='坐席':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="agId"]').click()
            elif    new_objtype=='业务组':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="grpId"]').click()  #
            elif    new_objtype=='技能组':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="callQue"]').click()
            elif    new_objtype=='号码组':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="number"]').click()
            elif new_objtype == '呼叫中心':
                self.wd.find_element_by_css_selector('input.ant-radio-input[value="callcenter"]').click()
            else:
                print('%s,无此对象类型'%(new_objtype))

        if new_roles !=None:    #修改可见范围
            while True:
                  #尝试找dels是否存在，如果不存在，直接点击可见范围选择角色；如果存在，则删除所有可见范围
                self.wd.implicitly_wait(1)
                dels = self.wd.find_elements_by_css_selector \
                        ('div .ant-select-selection ul > li.ant-select-selection__choice>span')
                if dels ==[]:
                    break
                    # if dels:    #如果dels为空，则为false
                for i in dels:  # 删除所有可见范围
                        i.click()
                self.wd.implicitly_wait(10)
            self.wd.find_element_by_css_selector(
                '#root div.add-template-col-wrap>div .ant-select-selection').click()  # 点击可见范围
            time.sleep(0.25)
            roles1=self.wd.find_elements_by_css_selector('ul[role="listbox"]>li')
            if type(new_roles) == type('str'):  # 如果传的是单个字符串参数,选择可见范围角色
                for i in range(len(roles1)):
                    if new_roles == roles1[i].text:
                        roles1[i].click()
            else:
                # self.wd.find_element_by_css_selector('div.add-template-col-title').click()   #点击无效区域
                for i in range(len(new_roles)):    # 选择可见范围角色
                    for j in range(len(roles1)):
                        if new_roles[i]==roles1[j].text:
                            roles1[j].click()
            # self.wd.find_element_by_css_selector('li[filename="%s"]'%roles).click()
            self.wd.find_element_by_css_selector('div.add-template-col-title').click()  # 点击无效区域

        if new_content!=None:   #修改模板描述
            self.wd.find_element_by_css_selector('textarea[placeholder="请输入模板描述内容"]').clear()
            self.wd.find_element_by_css_selector('textarea[placeholder="请输入模板描述内容"]').send_keys(new_content)

        if  new_report_type!=None:
            eles = self.wd.find_elements_by_css_selector(
                '.ant-row-flex .ant-checkbox-group span.ant-checkbox')  # 获取所有的报表类型
            for i in eles:  # 取消勾选所有报表类型
                if 'ant-checkbox-checked' in i.get_attribute('class'):
                    i.click()

            eles1=self.wd.find_elements_by_css_selector('.ant-row-flex .ant-checkbox-group label>span:nth-of-type(2)')
            if type(new_report_type) == type('str'):  # 如果传的是单个字符串参数
                for i in range(len(eles1)):
                    if new_report_type == eles1[i].text:
                        eles1[i].click()
            else:
                for i in range(len(new_report_type)): #多选报表类型
                    for j in range(len(eles1)):
                        if new_report_type[i]==eles1[j].text:
                            eles1[j].click()

        if new_data !=None:
            self.wd.find_element_by_css_selector('div.add-template-col-wrap > button:nth-child(2)').click()
            # 选择指标
            self.wd.implicitly_wait(1)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=1000")
            time.sleep(0.5)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=2000")
            time.sleep(0.5)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=3000")
            time.sleep(0.5)
            self.wd.execute_script("document.getElementsByClassName('ant-transfer-list-content')[0].scrollTop=4000")
            time.sleep(0.5)
            self.wd.implicitly_wait(10)
            eles2 = self.wd.find_elements_by_css_selector('ul.ant-transfer-list-content>div')  # 取到所有个指标
            text = self.wd.find_elements_by_css_selector('ul.ant-transfer-list-content>div span.custom-item')
            checkbox = self.wd.find_elements_by_css_selector('ul.ant-transfer-list-content>div .ant-checkbox')
            cont = []
            for i in text:
                cont.append(i.text)
            if type(new_data) == type('str'):  # 如果传的是单个字符串参数
                for i in range(len(cont)):
                    if new_data == cont[i]:
                        checkbox[i].click()
            else:
                for i in range(len(new_data)):
                    for j in range(len(eles2)):
                        # if data[i]==eles2[j].find_element_by_css_selector('span.custom-item').text: #判断名称是否相同
                        if new_data[i] == cont[j]:
                            # if data[i] not in cont[j]:
                            # eles2[j].find_element_by_css_selector('.ant-checkbox').click()     #点击勾选框
                            checkbox[j].click()
                    if new_data[i] not in cont:
                        print('%s指标错误' % (new_data[i]))
        self.wd.find_element_by_css_selector('div.ant-transfer-operation > button:nth-child(2)').click()  # 向右
        self.wd.find_element_by_css_selector('button[type="submit"]').click()  # 保存模板按钮
        time.sleep(1.5)

    def delAll_ReportTemplate(self):
        Custom_reportLib().go_listReportTemplate()
        time.sleep(1)
        self.wd.implicitly_wait(1)
        while True:
            del_button = self.wd.find_elements_by_css_selector('div > i.iconfont.icon-trash')
            if del_button == []:
                break
            del_button[0].click()
            time.sleep(0.5)
            self.wd.find_element_by_css_selector \
                ('div.ant-modal-footer >div > button.ant-btn.ant-btn-primary').click()
            time.sleep(2)
        self.wd.implicitly_wait(10)


if __name__ == '__main__':
    t1=WebOpLib()
    t1.open_browser()
    t1.login('wuhan','1234',123456)
    t2=Custom_reportLib()
    t2.go_listReportTemplate()
    t2.addReportTemplate(name='auto坐席报表指标集',index='坐席工作表现报表指标集')
    # t2.update_ReportTemplate(name='auto坐席报表tc001007',new_name='newname',new_roles='全部角色',new_content='autoRFS'
    #                          ,new_report_type='半小时明细',new_data='呼入量')
    # t2.delAll_ReportTemplate()
