from pylibrary.test_pylib import *
from pylibrary.online_pylib import *
import unittest
import csv

listFinal=[]  #写入csv的结果

# skipList=[]

# shouldSkip = [ "10秒接听量"]

class   Monitor(ParametrizedTestCase):
    '''自定义报表测试环境数据与线上数据对比_接口测试用例'''

    #读取csv里的所有指标参数。开始读文件之前把所有,pass替换掉为空
    rlist=[]  #清除掉pass和fail的列表
    with open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\test_online_report_data.csv', 'r'
            ,encoding="utf-8") as f:
        for yy in f.readlines():
            yy = yy.replace(',pass', '')   #替换
            yy = yy.replace(',fail','')
            rlist.append(yy)   #清除pass和fail的列表
    out = open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\test_online_report_data.csv', 'w', encoding="utf-8",
               newline='')  #写数据
    writer = csv.writer(out)

    for i in rlist:
        xyz=[]
        yz=i.split(",")  #分割csv里的每一行为列表
        if len(yz) >= 10 and len(yz) <=12:
            del yz[9:11]
        for j in yz:
            xyz.append(j.replace("\n",''))
        writer.writerow(tuple(xyz))   #重新将元祖写进csv

    out.close()

    date = csv.reader(open('D:\\IC\\other\\Python_code\\CTI_report\\ini\\test_online_report_data.csv', 'r',
                           encoding="utf-8"))  #重新读分为列表的csv

    list1 = []    #取csv的列表
    for i in date:
        list1.append(i)
    del list1[0]
    # paramtext = list1[0]
    for paramtext in list1:
        for i in range(len(paramtext)):
            if paramtext[i]=='':
                 paramtext[i]=None
    print('list1:'+str(len(list1)),list1)
    def test_OnlineReport(self):
        '''测试环境与线上环境-日报指标测试用例'''
        # 线上环境返回查询所有的报表数据
        online_report_num_all=None
        test_report_num_all = None
        try:
            self.a=0
            online_report_num_all = Online_PyLib().getAgReport(self.param[0], self.param[1], self.param[2],
                                                        self.param[3], self.param[4], self.param[5], self.param[6])
            self.a=1
            self.online_report_num = online_report_num_all[0][self.param[7]]     # 线上查询结果

            self.a=2
            # 测试环境返回查询所有的报表数据
            test_report_num_all = PyLib().getAgReport(self.param[0], self.param[1], self.param[2], self.param[3]
                                                      , self.param[4], self.param[5], self.param[6])
            self.test_report_num = test_report_num_all[0][self.param[7]]  # 测试环境查询结果,正常返回是int
            self.a=3
        except Exception as msg:
            if self.a==0:
                print('线上getAgReport的返回结果有问题：',online_report_num_all)
            if self.a==1:
                print('线上环境获取指标数值失败，查询报表返回结果：', online_report_num_all)
                if msg:
                    self.online_report_num=None
            if self.a==2:
                print('测试环境获取指标数值失败，查询报表返回结果：', test_report_num_all)
                if msg:
                    self.test_report_num = None

        finally:
            jieguo = []  # 加入执行结果
            o_result=[]  #线上接口查询结果
            t_result=[]  #测试环境接口查询结果
            if self.a==3:
                if self.online_report_num == self.test_report_num:
                    jieguo.append('pass')
                    o_result.append(self.online_report_num)
                    t_result.append(self.test_report_num)
                else:
                    jieguo.append('fail')
                    o_result.append(self.online_report_num)
                    t_result.append(self.test_report_num)
            else:
                jieguo.append('fail')
                o_result.append(self.online_report_num)
                t_result.append(self.test_report_num)
            # listFinal.append(self.param + jieguo)
            listFinal.append(self.param + o_result + t_result + jieguo)  #把线上数据、测试环境数据、最终pass/fail加到csv中
            # print(listFinal)

        if  self.param[3] != None:
            print(self.param[8], ':', self.param[0], '模板名为“', self.param[2], '” 坐席工号为“',  #打印详情：xx进线量：10-28日，模板名称为xxx，技能组名称为：xxx，报表的查询结果是：
                  self.param[3],'”测试环境查询结果是：', self.test_report_num,',线上环境查询结果是：',
                  self.online_report_num)
        elif  self.param[4] != None:
            print(self.param[8], ':', self.param[0], '模板名为“', self.param[2], '” 技能组名称为“',    #打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                  self.param[4], '”测试环境查询结果是：', self.test_report_num,',线上环境查询结果是：',
                  self.online_report_num)
        elif  self.param[5] != None:
            print(self.param[8], ':', self.param[0], '模板名为“', self.param[2], '” 业务组名称为“',    #打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                  self.param[5], '”测试环境查询结果是：', self.test_report_num,',线上环境查询结果是：',
                  self.online_report_num)
        elif  self.param[6] !=None:
            if self.param[6] == '0':                # 打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                print(self.param[8], ':', self.param[0], '模板名为“', self.param[2], '” 号码组名称为“默认号码组”，'
                        '测试环境查询结果是：', self.test_report_num,',线上环境查询结果是：',self.online_report_num)
            else:
                print(self.param[8], ':', self.param[0], '模板名为“', self.param[2], '” 号码组名称为“',self.param[6],  # 打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                        '”测试环境查询结果是：', self.test_report_num,',线上环境查询结果是：',self.online_report_num)
        else:
            print(self.param[8], ':', self.param[0], '模板名为“', self.param[2], '”,“ 呼叫中心 '  # 打印详情：xx进线量：10-28日，模板名称为xxx，坐席名称为：xxx，报表的查询结果是：
                  , '”测试环境查询结果是', self.test_report_num,',线上环境查询结果是：',self.online_report_num)

        self.assertEqual(self.online_report_num, self.test_report_num)   #断言

if  __name__ == '__main__':
    unittest.main(verbosity=2)
    # now = time.strftime("%Y-%m-%d %H_%M_%S")
    #
    # htmlfile = 'D:\\IC\\other\\Python_code\\CTI_report\\report\\'
    # suite = unittest.TestSuite()  #构造测试集
    # suite.addTest(InterfaceReport1('test_Agreport1'))
    # BeautifulReport(suite).report(filename='测试报告'+now,description='自定义坐席测试报告',log_path=htmlfile)


