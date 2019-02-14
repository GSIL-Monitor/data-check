#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from pylibrary.py_agent import  PyAgent
from pylibrary.test_pylib import *
from parameterized import parameterized



class   InterfaceReport(unittest.TestCase):
    '''明细报表(坐席、呼入、技能组)与自定义报表坐席指标对比接口测试用例'''
    # case_path = os.path.join(os.getcwd())
    # report_path = os.path.join(os.getcwd(), 'report')
    # print(report_path)
    # @parameterized.expand(['2018-09-13 00:00:00', '2018-09-13 23:59:59', '2001','2018-09-13','2018-09-13','测试'])

    def test_TotalCallNum_ACD_IB(self):  #ACD呼入量
        '''ACD呼入量'''
        self.ACD_detail_num  =   PyAgent().TotalCallNum_ACD_IB('2018-09-13 00:00:00',
                                                              '2018-09-13 23:59:59','2001')
        self.ACD_report_num  =   PyLib().getAgReport('2018-09-13','2018-09-13','测试',
                                                   '2001')[0]['TotalCallNum_ACD_IB']
        self.assertEqual(self.ACD_detail_num,self.ACD_report_num)

    def test_TotalCallAnsweredNum_IN(self):  #总呼入接通量
        '''总呼入接通量'''
        self.TotalCallIN_detail = PyAgent().TotalCallAnsweredNum_IN('2018-09-13 00:00:00',
                                                              '2018-09-13 23:59:59','2001')
        self.TotalCallIN_report = PyLib().getAgReport('2018-09-13','2018-09-13','测试',
                                                   '2001')[0]['TotalCallAnsweredNum_IN']
        self.assertEqual(self.TotalCallIN_detail, self.TotalCallIN_report)

    def test_RingNum_IB(self):  #呼入振铃次数
        '''呼入振铃次数'''
        self.RingNum_IB_detail = PyAgent().RingNum_IB('2018-09-13 00:00:00',
                                                              '2018-09-13 23:59:59','2001')
        self.RingNum_IB_report = PyLib().getAgReport('2018-09-13','2018-09-13','测试',
                                                   '2001')[0]['RingNum_IB']
        self.assertEqual(self.RingNum_IB_detail,self.RingNum_IB_detail)

    def test_TotalCallNum_Transfer_IB(self):  #"被转接客户量"
        '''被转接客户量'''
        self.num = 4
        self.TotalCallNum_Transfer_IB=PyLib().getAgReport('2018-09-13','2018-09-13','测试',
                                                   '2001')[0]['TotalCallNum_Transfer_IB']
        self.assertEqual(self.num,self.TotalCallNum_Transfer_IB)

if  __name__ == '__main__':

    unittest.main(verbosity=2)

