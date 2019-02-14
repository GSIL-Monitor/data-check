#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pylibrary.test_pylib import PyLib,ParametrizedTestCase
import unittest
import csv

listFinal=[]

class   TestMonitor(ParametrizedTestCase):
    '''自定义报表与实际数据对比接口测试用例'''

    #读取csv里的所有指标参数。开始读文件之前把所有,pass替换掉为空
    rlist=[]  #清除掉pass和fail的列表
    with open('D:\\IC\\other\\Python_code\\manage_unittest\\ini\\test_report_data.csv', 'r',encoding="utf-8") as f:
        for yy in f.readlines():
            #line = yy.strip().split()
            yy = yy.replace(',pass', '')   #替换
            yy = yy.replace(',fail','')
            rlist.append(yy)
    out = open('D:\\IC\\other\\Python_code\\manage_unittest\\ini\\test_report_data.csv', 'w', encoding="utf-8",newline='')
    writer = csv.writer(out)

    for i in rlist:
        xyz=[]
        yz=i.split(",")
        for j in yz:
            xyz.append(j.replace("\n",''))
        writer.writerow(tuple(xyz))
    out.close()

    date = csv.reader(open('D:\\IC\\other\\Python_code\\manage_unittest\\ini\\test_report_data.csv', 'r',encoding="utf-8"))

    list1 = []
    for i in date:
        list1.append(i)
    del list1[0]
    # paramtext = list1[0]
    for paramtext in list1:
        for i in range(len(paramtext)):
            if paramtext[i]=='':
                 paramtext[i]=None

    print('222',list1)
    # print(222)
    # list1 = [
    #     ('2018-09-26', '2018-09-26', '坐席指标测试', '2001', None, 49, 'TotalCallNum_ACD_IB', 'ACD呼入量'),
    #     ('2018-09-27', '2018-09-27', '坐席指标测试', '2001', None, 3, 'TotalCallNum_Transfer_IB', '被转接客户量'),
    #     ('2018-09-26', '2018-09-26', '坐席指标测试', '2001', None, 11, 'TotalCallNum_Disconnect_IB', '强拆客户量'),
    #     ('2018-09-13', '2018-09-13', '坐席指标测试', '2001', None, 8, 'TotalCallNum_Direct_Inter_IN', '内部呼入量'),
    #     ('2018-09-13', '2018-09-13', '坐席指标测试', '2001', None, 2, 'TotalCallNum_Transfer_Inter_IN', '被转接坐席量'),
    #     ('2018-09-13', '2018-09-13', '坐席指标测试', '2001', None, 5, 'TotalCallNum_Disconnect_Inter_IN', '强拆坐席量'),
    #     ('2018-09-28', '2018-09-28', '坐席指标测试', '2001', None, 1, 'TotalCallNum_Directed_Inter_IN', '被内部直呼量'),
    #     ('2018-09-13', '2018-09-13', '坐席指标测试', '2001', None, 8, 'TotalCallNum_Consulted_Inter_IN', '被咨询量'),
    #     ('2018-09-26', '2018-09-26', '坐席指标测试', '2001', None, 49, 'TotalCallAnsweredNum_ACD_IB', 'ACD呼入接通量'),
    #     ('2018-09-13', '2018-09-13', '坐席指标测试', '2001', None, 4, 'TotalCallAnsweredNum_TakeTransfer_IB', '被转接客户接通量'),
    #     ('2018-09-26', '2018-09-26', '坐席指标测试', '2001', None, 11, 'TotalCallAnsweredNum_Disconnect_IB', '强拆客户接通量'),
    #     ('2018-09-13', '2018-09-13', '坐席指标测试', '2001', None, 8, 'TotalCallAnsweredNum_Direct_Inter_IN', '内部呼入接通量'),
    #     ('2018-09-26', '2018-09-26', '坐席指标测试2', '2001', None, 88, 'TotalRingNum', '总振铃次数'),
    #     ('2018-09-17', '2018-09-17', '技能组测试', None, 'BI技能组', 87, 'TotalEnterNum', '总进线量'),
    #     ('2018-09-17', '2018-09-17', '技能组测试', None, 'BI技能组', 77, 'TotalAnboundNum', '呼损量'),
    #     ('2018-09-17', '2018-09-17', '技能组测试', None, 'BI技能组', 28, 'AbandonedNum_Full', '满队列溢出量'),
    #     ('2018-09-17', '2018-09-17', '技能组测试', None, 'BI技能组', 5, 'AbandonedNum_NoAgent', '无坐席溢出量')
    # ]
    def test_Report(self):
        '''坐席 指标测试'''
        self.num = self.param[5]   #页面已经查询好的值
        self.report_num1 = PyLib().getAgReport(self.param[0],self.param[1],self.param[2],self.param[3],self.param[4])  #Post请求获取页面查询结果
        self.report_num=self.report_num1[0][self.param[6]]  #获取具体的指标值
        # print(self.param[5], ':', self.param[0], '模板名为“', self.param[1], '” 坐席工号为“', self.param[2],
        #       '”报表的查询结果是',self.report_num)
        self.assertEqual(self.num,self.report_num)   #断言

    def test_QueReport(self):
        '''日报指标测试'''
        bug1102 = str(self.param[7])
        self.num = int(bug1102.split('.')[0])
        report_num_all = None
        #开始时间,结束时间,自定义报表模板名称,坐席工号,技能组名称,业务组名称,中继/呼叫中心,页面查询结果(预期结果),指标名称(英文),指标中文名称,结果

        try:
            self.a = 0
            report_num_all = PyLib().getAgReport(self.param[0], self.param[1], self.param[2], self.param[3]
                                                 # 返回查询所有的报表数据
                                                 , self.param[4], self.param[5], self.param[6])
            self.a = 1
            self.report_num = report_num_all[0][self.param[8]]  # 获取具体的指标值['AbandonedNum_NoAgent'],正常返回是int

            self.a = 2
        except BaseException as msg:
            if self.a == 0:
                print('测试环境getAgReport的返回结果有问题：',report_num_all)
            if self.a == 1:
                print('获取指标数值失败，查询报表返回结果：', report_num_all)
                if msg:
                    self.report_num=None
        finally:
            jieguo = []  # 加入执行结果
            t_result = []  #测试接口查询结果
            if self.a ==2:
                if self.num == self.report_num:
                    jieguo.append('pass')
                    t_result.append(self.report_num)
                else:
                    jieguo.append('fail')
                    t_result.append(self.report_num)
            else:
                jieguo.append('fail')
                t_result.append(self.report_num)
            listFinal.append(self.param + t_result + jieguo)  #把测试接口查询结果、最终结果pass or fail添加到csv中

        if  self.param[3] != None:
            print(self.param[9], ':', self.param[0], '模板名为“', self.param[2], '” 坐席工号为“',  #打印详情：xx进线量：10-28日，模板名称为xxx，技能组名称为：xxx，报表的查询结果是：
                  self.param[3],'”报表的查询结果是', self.report_num)
        elif  self.param[4] != None:
            print(self.param[9], ':', self.param[0], '模板名为“', self.param[2], '” 技能组名称为“',    #打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                  self.param[4], '”报表的查询结果是', self.report_num)
        elif  self.param[5] != None:
            print(self.param[9], ':', self.param[0], '模板名为“', self.param[2], '” 业务组名称为“',    #打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                  self.param[5], '”报表的查询结果是', self.report_num)
        elif  self.param[6] !=None:
            if self.param[6] == '0':                # 打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                print(self.param[9], ':', self.param[0], '模板名为“', self.param[2], '” 号码组名称为“默认号码组”，报表的查询结果是', self.report_num)
            else:
                print(self.param[9], ':', self.param[0], '模板名为“', self.param[2], '” 号码组名称为“',  # 打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                      self.param[6], '”报表的查询结果是', self.report_num)
        else:
            print(self.param[9], ':', self.param[0], '模板名为“', self.param[2], '”,“ 呼叫中心 '  # 打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                  , '”报表的查询结果是', self.report_num)
        self.assertEqual(self.num, self.report_num)             #断言self.num





    # def test_Agreport1(self,start_time,end_time,template_name,ag_num,testData,reportData):
    #     self.num = testData
    #     self.report_num1 = PyLib().getAgReport(start_time,end_time,template_name,ag_num)
    #     self.report_num=self.report_num1[0][reportData]
    #     self.assertEqual(self.num,self.report_num)




if  __name__ == '__main__':
    unittest.main(verbosity=2)
    # now = time.strftime("%Y-%m-%d %H_%M_%S")
    #
    # htmlfile = 'D:\\IC\\other\\Python_code\\manage_unittest\\report\\'
    # suite = unittest.TestSuite()  #构造测试集
    # suite.addTest(InterfaceReport1('test_Agreport1'))
    # BeautifulReport(suite).report(filename='测试报告'+now,description='自定义坐席测试报告',log_path=htmlfile)

