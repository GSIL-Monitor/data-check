#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pylibrary.test_pylib import PyLib
from cfg import *
import time,datetime
import requests
import json

class PyAgent:
    '''在manage明细报表中（呼入、坐席、技能组明细报表），查询指标结果'''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'   #RFS框架对接

    def __init__(self):
        self.header = {'Content-Type': 'application/json;charset=UTF-8',"Accept": "application/json, text/plain, */*"}
        self.header1 = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   "X-Requested-With": "XMLHttpRequest", "Accept": "application/json, text/javascript, */*; q=0.01"
                   }

        self.cookie = {'manage_access_token': manage_token, 'PHPSESSID': test_phpsessid} #测试
        self.cookie2={'manage_access_token': manage_token, 'PHPSESSID': PHPSESSID}  #线上报表token，线上老系统数据
        # self.cookie3={'manage_access_token': test_manage_token, 'PHPSESSID': test_phpsessid,'HMACCOUNT':test_HMACCOUNT}
        self.t = int(time.time())   #10位
        self.ndt = int(time.time() * 1000)   #13位
    
    def getAgDetail(self,start_time,end_time,ag_num,result="-1",ag_phone="",cus_phone='',call_type='-1'
                    ,endresult="-1",que_id="-1",call_id="",group_id="-1",_search="false",rows=100,page=1
                    ,sidx="start_time",sord="desc"):
        # 查询老系统坐席明细报表所有内容
        '''
        :param start_time: 开始时间
        :param end_time:结束时间
        :param agIds:查询的坐席id
        :param result: 呼叫结果 '-1':'全部';'0':接通;'1'：‘振铃放弃’;'2'：‘未接’
        :param ag_phone:坐席号码
        :param cus_phone: 客户号码
        :param call_type: 呼叫类型 "-1":全部；"1"：呼出；"2":呼入；"3":呼出转接；"4"：呼入转接；‘5’:呼出拦截；‘6’：呼入拦截
                                    ‘7’：被咨询；‘8’：监听
        :param endresult: 结束类型
        :param que_id: 技能组id
        :param call_id: 呼叫id
        :param group_id: 业务组id
        :param _search:
        :param rows: 显示行数
        :param page: 显示页数
        :param sidx:
        :param sord: 排序，默认倒序
        :return:返回坐席明细报表查询内容
        '''
        if  call_type !='-1':
            if  call_type=='呼出':
                call_type='1'
            elif    call_type=='呼入':
                call_type='2'
            elif    call_type=='呼出转接':
                call_type='3'
            elif    call_type=='呼入转接':
                call_type='4'
            elif    call_type=='呼出拦截':
                call_type='5'
            elif    call_type=='呼入拦截':
                call_type='6'
            elif    call_type=='被咨询':
                call_type='7'
            elif    call_type=='监听':
                call_type='8'

        if  result !='-1':
            if  result=='接通':
                result='0'
            elif    result=='振铃放弃':
                result='1'
            elif    result=='未接':
                result='2'

        if ag_num!='-1':
            self.ag_id=PyLib().getAgid(ag_num)
        elif ag_num=='-1':
            self.ag_id=ag_num

        params={"ag_num":self.ag_id,"result":result,"ag_phone":ag_phone,"cus_phone":cus_phone,"call_type":call_type,
                 "endresult":endresult,"que_id":que_id,"call_id":call_id,"group_id":group_id,"start_time":start_time
                ,"end_time":end_time}
        param=json.dumps(params)
        pload={"param":param,"_search":_search,"rows":rows,"page":page,"sidx":sidx,"sord":sord,"nd":self.ndt}
        response=requests.post('http://m.icsoc.net/report/detail/call/list',data=pload,cookies=self.cookie2
                               ,headers=self.header1)

        res=response.text
        if res.__contains__('欢迎用户登录'):
            raise Exception("鉴权失败, 请重新登录")
        else:
            ret=response.json()
        return ret

    #
    # def __init__(self):
    #     '''呼入明细报表接口的request headers'''
    #
    #     self.header={'Content-Type':'application/json'}
    #     self.header1={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    #                   "X-Requested-With": "XMLHttpRequest","Accept":"application/json, text/javascript, */*; q=0.01"
    #                   }
    #     self.cookie={'manage_access_token':manage_token,'PHPSESSID':PHPSESSID}   #呼入明细报表页面的token，使用线上的token和sessid
    #     self.t=int(time.time())   #时间参数
    #     self.ndt = int(time.time() * 1000)  #11位数的时间参数

    def cus_num(self,res):
        ''' 统计坐席号码为空、客户号码为坐席的数量'''
        #res：明细报表接口请求后的json数据

        agnull_num = 0  # 坐席号码为空的数量
        cus_num = 0  # 客户号码为坐席的数量
        for i in res['rows']:
            if i['ag_phone'] == '':
                agnull_num += 1
            elif len(i['cus_phone']) <= 5:
                cus_num += 1
        total=agnull_num+cus_num  #坐席号码、客户号码为空的坐席数量
        return total

    def TotalCallNum_ACD_IB(self,start_time,end_time,ag_num='-1',rows=1000):
        '''用明细报表计算ACD呼入量'''

        res=PyAgent().getAgDetail(start_time=start_time,end_time=end_time
                           ,ag_num=ag_num,call_type='呼入',rows=rows)
        null_num=PyAgent().cus_num(res)   #去掉坐席号码为空、客户号码为坐席的数量

        total=res['records']-null_num     #返回ACD呼入量
        return total

    def TotalCallAnsweredNum_IN(self,start_time,end_time,ag_num="-1",rows=1000):
        '''用明细报表计算总呼入接通量'''
        huru=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼入',result='接通',rows=rows)['records']
        huchuzj=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼出转接',result='接通',rows=rows)['records']
        huruzj =PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼入转接',result='接通',rows=rows)['records']
        huchulj=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼出拦截',result='接通',rows=rows)['records']
        hurulj=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼入拦截',result='接通',rows=rows)['records']
        beizx=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='被咨询',result='接通',rows=rows)['records']

        total=huru+huchuzj+huruzj+huchulj+hurulj+beizx
        return  total

    def TotalCallAnsweredNum_IN2(self,start_time,end_time,ag_num="-1",rows=1000):
        '''用明细报表计算总呼入接通量'''
        param_call_type = {'呼入','呼出转接','呼入转接','呼出拦截','呼入拦截','被咨询'}
        total=0
        for i in param_call_type:
            total+=PyAgent().getAgDetail(start_time=start_time, end_time=end_time, ag_num=ag_num,
                                call_type=i, result='接通', rows=rows)['records']
        return  total

    def RingNum_IB(self,start_time,end_time,ag_num="-1",rows=1000):
        '''用明细报表计算呼入振铃次数'''

        huru=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼入',rows=rows)
        null_num1=PyAgent().cus_num(huru)

        huchuzj=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼出转接',rows=rows)
        null_num2 = PyAgent().cus_num(huchuzj)

        huruzj=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼入转接',rows=rows)
        null_num3 = PyAgent().cus_num(huruzj)

        huchulj=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼出拦截',rows=rows)
        null_num4 = PyAgent().cus_num(huchulj)

        hurulj=PyAgent().getAgDetail(start_time=start_time,end_time=end_time,ag_num=ag_num,
                                 call_type='呼入拦截',rows=rows)
        null_num5 = PyAgent().cus_num(hurulj)

        null_num_total=null_num1+null_num2+null_num3+null_num4+null_num5    #坐席工号，客户号码为空的总数
        total =huru['records']+huchuzj['records']+huruzj['records']+huchulj['records']+hurulj['records']-null_num_total

        return total

    def RingTime_IB(self,start_time,end_time,ag_num="-1",rows=1000):
        '''用明细报表计算呼入振铃总时长'''

        time=0
        huru = PyAgent().getAgDetail(start_time=start_time, end_time=end_time, ag_num=ag_num,
                                   call_type='呼入', rows=rows)['rows']

        endtime_stamp=datetime.datetime.strptime(huru[0]['end_time'], "%Y-%m-%d %H:%M:%S")
        starttime_stamp=datetime.datetime.strptime(huru[0]['start_time'], "%Y-%m-%d %H:%M:%S")

        if  '接通' in huru[0]['result']:
            pass
        else:
            time1=endtime_stamp-starttime_stamp
            time+=time1
        print(time)


    def CallNum_OB(self):   #外呼量
        pass

    def CallAnsweredNum_OB(self):   #外呼接通量
        pass

    def TalkTime_OB(self): #外呼通话时长
        pass

    def TotalLoginTime(self):  #总登录时长
        pass

    def NotReadyTime(self):  #总置忙时长
        pass




if __name__ == '__main__':
    t1 = PyAgent().TotalCallAnsweredNum_IN2("2018-09-13 00:00:00", "2018-09-13 23:59:59", '2001')
    print(t1)
    # t2=PyAgent().RingTime_IB('2018-08-17 00:00:00','2018-08-17 23:59:59','2001')
    # print(t2)


