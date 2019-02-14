#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
from cfg import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest


postList2=[]
postMap2={}

AgidpostList2=[]
AgidpostMap2={}

QuepostList2=[]
QuepostMap2={}

GrouppostList2=[]
GrouppostMap2={}

TemppostList2=[]
TemppostMap2={}

RolepostList2=[]
RolepostMap2={}

ServerpostList2=[]
ServerpostMap2={}

class PyLib:
    '''使用接口查询自定义报表数据'''
    # ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.header = {'Content-Type': 'application/json;charset=UTF-8',"Accept": "application/json, text/plain, */*"}
        self.header1 = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   "X-Requested-With": "XMLHttpRequest", "Accept": "application/json, text/javascript, */*; q=0.01"
                   }
        self.cookie = {'manage_access_token': manage_token, 'PHPSESSID': test_phpsessid} #测试
        self.cookie2={'manage_access_token': manage_token, 'PHPSESSID': PHPSESSID}  #线上报表token，线上老系统数据
        self.t = int(time.time())   #10位
        self.ndt = int(time.time() * 1000)   #13位
        # print(self.t)

    def postSet2(self, hx, postList, postMap, postUrl, datas, cookie, header):
        '''
        方法是為了判斷是否需要進行post，是否需要的判定條件是hx
        :param hx: 表示方法各參數相加起來的合值，若合值相同，則無需post，反之。
        :param postList: 在post之前，判斷hx是否在list中，若不在，表示之前從未post過，那就進行post，且將hx放入list中
        :param postMap: post之後將hx作為key，response作為value放入map中，後續若無需post，則用hx取出response即可。
        :param postUrl: 各post方法的地址
        :param datas: 因為各方法的data值略有不同，故傳值。
        :param cookie: 因為各方法的data值略有不同，故傳值。
        :param header: 因為各方法的data值略有不同，故傳值。
        :return: response即為post結果
        '''
        if hx not in postList:  # 若不在，就放進去
            postList.append(hx)
            if datas == None:
                response = requests.post(postUrl, cookies=cookie, headers=header)
            else:
                response = requests.post(postUrl, data=datas, cookies=cookie, headers=header)
            postMap[hx] = response
        else:
            response = postMap[hx]
        return response

    def getAgid(self,ag_num='',user_role='all'):  #查询线上坐席id
        '''
        :param ag_num: 坐席工号
        :return: 坐席Id
        '''
        params={'keyword':ag_num,'user_role':user_role}
        data=json.dumps(params)
        datas={'filter':data,'sord':'desc'}
        hx = str(ag_num) + str(user_role)
        response = self.postSet2(hx, AgidpostList2, AgidpostMap2, 'http://m.icsoc.net/agent/list', datas, self.cookie2,
                                self.header1)
        ret = response.json()
        if ret == '鉴权失败, 请重新登录':
            raise Exception("鉴权失败, 请重新登录")
        return ret['rows'][0]['ag_id']

    def getQueid(self,que_name=''):  #查询线上技能组Id
        '''
        :param que_name: 技能组名称
        :return:  技能组id
        '''
        params={'keyword':que_name}
        data=json.dumps(params)
        datas={'filter':data,'sord':'desc'}
        hx = str(que_name)
        response = self.postSet2(hx, QuepostList2, QuepostMap2, 'http://m.icsoc.net/queue/list', datas, self.cookie2,
                                self.header1)
        ret = response.json()
        # print(str(ret))
        if 'message' in ret:
            if ret['message'] == '鉴权失败, 请重新登录':
                raise Exception("鉴权失败, 请重新登录")
        return ret['rows'][0]['id']

    def getGroupid(self,group_name=''):  #查询线上业务组id
        params = {'keyword': group_name}
        data = json.dumps(params)
        datas = {'fliter': data,"sidx":"group_id","nd":self.ndt,"_search":"false","sort":"desc"}
        hx = str(group_name)
        response = self.postSet2(hx, GrouppostList2, GrouppostMap2, 'http://m.icsoc.net/business/list', datas,
                                self.cookie2, self.header1)
        ret = response.json()
        # print(ret)
        if ret['message'] == '鉴权失败, 请重新登录':
            raise Exception("鉴权失败, 请重新登录")
        return ret['rows'][0]['group_id']   #返回业务组id

    # def getServerNumId1(self,servernum=''):  #查询号码组id
    #     params = {'keyword':servernum}
    #     data = json.dumps(params)
    #     datas = {'fliter':data,'sidx':'id','nd':self.ndt,'_search':'false','sort':'desc'}
    #     response = requests.post('http://m.icsoc.net/phone/group/list',data=datas,cookies=self.cookie2,
    #                              headers=self.header1)  #线上token
    #     ret = response.json()
    #     print(ret)
    #     id=0
    #     if ret['total'] == 0:   #如果没有号码组，返回id=0
    #         return 0
    #     else:
    #         if ret['message'] == '鉴权失败, 请重新登录':
    #             raise Exception("鉴权失败, 请重新登录")
    #         return ret['rows'][0]['id']    #返回号码组Id

    def getTempateId(self,temlate_name=None):  #获取测试环境模板列表id
        hx = str(temlate_name)
        response = self.postSet2(hx, TemppostList2, TemppostMap2,
                                'http://m-report-test.icsoc.net/api/manager-old-app/report/listReportByRole', None,
                                self.cookie2, self.header)
        ret = response.json()
        # print(ret)
        if ret['message'] =='鉴权失败, 请重新登录':    #鉴权
            raise Exception("鉴权失败, 请重新登录")
        elif ret['message']=='系统异常, 请联系管理员!':
            raise  Exception("系统异常, 请联系管理员!")
        myReportList=ret['data']['myReportList']
        if temlate_name !=None:
            for i in myReportList:
                if i['name'] ==temlate_name:
                    return i['id']
        else:
            ids=[]
            for i in myReportList:
                ids.append(i['id'])
            return ids

    def getroleId(self,template_name):  #获取测试环境角色Id
        template_id= PyLib().getTempateId(template_name)
        data={'id':template_id,'_t':self.t}
        datas=json.dumps(data)
        hx = str(template_name)
        response = self.postSet2(hx, RolepostList2, RolepostMap2,
                                'http://m-report-test.icsoc.net/api/manager-old-app/report/getReportTemplate', datas,
                                self.cookie2, self.header)
        ret = response.json()
        # print(ret)
        if ret['message'] == '鉴权失败, 请重新登录':
            raise Exception("鉴权失败, 请重新登录")
        roleId=ret['data']['selects'][0]['value']
        return roleId

    def getServerNumId(self,servernum_name=None,template_name=None):   #获取测试环境号码组id

        roleId=PyLib().getroleId(template_name)  #角色id

        data={'objType':'serverNum','roleId':roleId,'_t':self.t}
        datas=json.dumps(data)
        hx = str(servernum_name) + str(template_name)
        response = self.postSet2(hx, ServerpostList2, ServerpostMap2,
                                'http://m-report-test.icsoc.net/api/manager-old-app/report/getGroupByRole', datas,
                                self.cookie2, self.header)
        ret = response.json()
        # print(ret)
        if ret['message'] == '鉴权失败, 请重新登录':
            raise Exception("鉴权失败, 请重新登录")
        datalist=ret['data']['dataList']
        ids=[]
        if servernum_name==None:
            for i in datalist:
                ids.append(i['value'])
            return ids
        else:
            for i in datalist:
                if servernum_name==i['label']:
                    return i['value']

 #返回号码组列表，没有号码组时，返回0

    def getAgReport(self,startTime,endtime,templatename,ag_num=None,
                    que_name=None,grp_name=None,serverNums_name=None,reportType='日报'):
        '''查询测试环境自定义报表指标数据
        :param startTime: 开始时间
        :param endtime: 结束时间
        :param reportType: 报表类型--
        "PT30M_DETAIL"半小时明细  "PT30M_ADD"半小时叠加  "PT1H_DETAIL"小时明细  "PT1H_ADD"1小时叠加  "P1D_DETAIL"日报
        # "P1M_DETAIL" 月报
        :param templatename: 报表模板名称
        :param agIds:要查询的坐席id
        :return: 返回自定义报表查询结果
        '''
        pylib=PyLib()
        reportType = pylib.change_ReportType(reportType)  #日报替换为"P1D_DETAIL"

        agIds = pylib.double_choice_ag(ag_num)      #多选的情况--坐席工号

        queIds = pylib.double_choice_que(que_name)   # 多选的情况--队列名称

        grpIds = pylib.double_choice_group(grp_name)  #业务组 grpIds

        servernum_ids = pylib.double_choice_servernum(serverNums_name,templatename) #号码组

        #获取模板列表id
        self.templateId = pylib.getTempateId(templatename)

        playload={"startTime":startTime,"endTime":endtime,"reportType":reportType, "_t":self.t,
                  "templateId":self.templateId,"agIds":agIds,"callQues":queIds,'pageNo':1,'pageSize':10,
                  "serverNums":servernum_ids,"grpIds":grpIds
                  }
        data=json.dumps(playload)  #转换为json
        hx = str(startTime) + str(endtime) + str(templatename) + str(ag_num) + str(que_name) + str(grp_name) + str(
            serverNums_name)
        response = self.postSet2(hx, postList2, postMap2, 'http://m-report-test.icsoc.net/api/dm-core/report/listReport', data,
                                self.cookie2, self.header)
        ret=response.json()
        # print(ret)
        pylib.auth(ret)  #鉴权
        if  ret['data']['reportData'] :
            return ret['data']['reportData']  # 返回查询报表的数据
        else:
            print('AgReport,reportData返回为空')
            return None

    def getReportTemplate_id(self,name="",objType="",roleIds=""):   #获取测试环境模板列表
        '''
        :param name: 查询报表名称
        :param objType: 对象类型
        :param roleIds: 可见范围
        :return: 返回模板列表json
        '''
        pload={"name":name,"objType":objType,"roleIds":roleIds,"_t":self.t}
        data=json.dumps(pload)
        response=requests.post('http://m-report-test.icsoc.net/api/manager-old-app/reportTemplate/listReportTemplate',
                               data=data,cookies=self.cookie,headers=self.header)
        ret=response.json()
        if ret == '鉴权失败, 请重新登录':
            raise Exception("鉴权失败, 请重新登录")
        return ret

    def change_ReportType(self,reportType):
        if reportType=='半小时明细':
            self.reportType='PT30M_DETAIL'
        elif    reportType=='半小时叠加':
            self.reportType='PT30M_ADD'
        elif    reportType=='小时明细':
            self.reportType='PT1H_DETAIL'
        elif    reportType=='小时叠加':
            self.reportType='PT1H_ADD'
        elif    reportType=='日报':
            self.reportType='P1D_DETAIL'
        elif    reportType=='月报':
            self.reportType='P1M_DETAIL'
        return self.reportType

    def double_choice_ag(self,ag_num):
        pylib = PyLib()
        agIds = ''  # 存多选坐席工号的字符串
        if ag_num != None:  # 判断坐席工号是否是none，如果是None：判断是不是多选，如果是多选，就按逗号切割，再请求坐席id，之后拼接逗号，传入带逗号格式的字符串
            if ',' in ag_num:
                for i in ag_num.split(','):  #
                    agIds += pylib.getAgid(i) + ','
                agIds = agIds[:-1]
            else:
                agIds = pylib.getAgid(ag_num)  # 看传参的坐席工号带不带逗号，如果不带逗号，就不做处理，直接请求id，
            # print(agIds)
        elif ag_num == None:
            agIds = None

        return agIds

    def double_choice_que(self,que_name):
        pylib = PyLib()
        queIds = ''
        if que_name != None:  # 判断队列名称是不是NONE
            if ',' in que_name:  # 如果是多选，就传带逗号的格式
                for i in que_name.split(','):  # 按逗号切割，请求到每个队列的id后，再拼接逗号，添加到queids字符串中
                    queIds += pylib.getQueid(i) + ','
                queIds = queIds[:-1]
            else:
                queIds = pylib.getQueid(que_name)
        elif que_name == None:
            queIds = None

        return queIds

    def double_choice_group(self,grp_name):
        pylib = PyLib()
        grpIds = ''
        if grp_name != None:  # 判断业务组名称是不是NONE
            if ',' in grp_name:  # 如果是多选，就传带逗号的格式
                for i in grp_name.split(','):  # 按逗号切割，请求到每个业务组的id后，再拼接逗号，添加到grpIds字符串中
                    grpIds += pylib.getGroupid(i) + ','
                    grpIds = grpIds[:-1]
            else:
                grpIds = pylib.getGroupid(grp_name)
        elif grp_name == None:
            grpIds = None

        return grpIds

    def double_choice_servernum(self,serverNums_name,templatename):
        pylib = PyLib()
        servernum_ids = ''  # 传入接口的号码组Id
        if serverNums_name != None:
            if ',' in serverNums_name:  # 如果是多选，就传带逗号的格式
                for i in serverNums_name.split(','):  # 按逗号切割，获取到每个号码组id后，再拼接
                    servernum_ids += str(pylib.getServerNumId(i, templatename)) + ','
                servernum_ids = servernum_ids[:-1]
            else:
                servernum_ids = pylib.getServerNumId(serverNums_name, templatename)  # 如果是单选，直接获取号码组id 0
        elif serverNums_name == 0:  # 如果参数是0，传入所有的号码组id，包括默认号码组
            list_ids = pylib.getServerNumId(template_name=templatename)
            for i in list_ids:
                servernum_ids += str(i) + ','
        elif serverNums_name == None:
            servernum_ids = None
        return servernum_ids

    def auth(self,ret):
        if 'message' in ret:
            if ret['message'] =='鉴权失败, 请重新登录':    #鉴权
                raise Exception("鉴权失败, 请重新登录")
            elif ret['message']=='系统异常, 请联系管理员!':
                raise  Exception("系统异常, 请联系管理员!")

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
    @staticmethod
    def parametrize(testcase_class,defName=None, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        if defName !=None:
            for name in testnames:
                if name==defName:
                    suite.addTest(testcase_class(name, param=param))
        else:
            for name in testnames:
                suite.addTest(testcase_class(name, param=param))
        return suite



if __name__ == '__main__':
    # t1=PyLib().getAgReport('2018-10-30','2018-10-30','坐席1.21','1023')
    # pprint.pprint(t1)
    # t2=PyLib().getAgDetail("2018-09-13 00:00:00", "2018-09-13 23:59:59", '2001')
    # print(t2)
    t3=PyLib().getReportTemplate_id()
    print(t3)
    a = '33'
    print(int(a.split('.')[0]))



