#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from interface.test_monitor import *
from BeautifulReport import BeautifulReport

if  __name__ == '__main__':

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(TestMonitor('test_Agreport1'))
    htmlfile = 'D:\\IC\\other\\Python_code\\CTI_report\\report\\'
    # fp = open(htmlfile, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='测试报告', description='用例执行情况')
    # runner.run(suite)
    # fp.close()
    suite = unittest.TestSuite()   #测试套件
    #suite.addTest(TestMonitor('test_Agreport1'))
    # for i in list:
    #     suite.addTest(ParametrizedTestCase.parametrize(TestMonitor, 'test_AgReport',param=i))
    skiplist = ['10秒接听量 ', '15秒接听量 ', '置闲次数', '20秒接听量 ', '25秒接听量 ', '30秒接听量 ', '10秒呼损量 ', '15秒呼损量 '
        , '20秒呼损量 ', '25秒呼损量 ', '30秒呼损量 ', '10秒放弃量 ', '15秒放弃量 ', '20秒放弃量 ', '25秒放弃量 ', '30秒放弃量 ']
    for i in TestMonitor.list1:

        suite.addTest(ParametrizedTestCase.parametrize(TestMonitor, 'test_QueReport',param=i))#测试用例加入到测试套件
    BeautifulReport(suite).report(filename='测试报告'+now,description='自定义报表-测试环境与实际页面数据对比'
                                  ,log_path=htmlfile)

    if len(listFinal)!=0:
        #生成报告后将finallist写入到csv中
        #先覆盖写第一句话
        out = open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\test_report_data.csv','w',
                   encoding="utf-8",newline='')
        writer=csv.writer(out)
        firstLine="开始时间","结束时间","自定义报表模板名称","坐席工号","技能组名称","号码组","呼叫中心",\
                  "指标名称(英文)","指标中文名称","预期结果(页面查询)","实际结果","结果"
        writer.writerow(firstLine)
        out.close()
        #然后追加新list
        out = open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\test_report_data.csv','a+',
                   encoding="utf-8",newline='')
        writer=csv.writer(out)
        for i in range(len(listFinal)):
            writer.writerow(listFinal[i])
        out.close()
