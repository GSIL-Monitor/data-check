#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pylibrary.test_pylib import PyLib
import json
import requests
from pylibrary.online_pylib import Online_PyLib

class Template(PyLib):
    '''使用接口增删改查模板'''

    #新增测试模板
    def AddTemplate(self,name,objType_name,rangeName,reportType_name='半小时明细,半小时叠加,小时明细,小时叠加,日报,周报'
                     ',月报',roleIds='all',roles='全部角色',status=1,remark=''):
        '''新增测试环境模板
        :param name: 模板名称
        :param objType_name: 对象类型--坐席
        :param rangeName: 指标名称
        :param reportType_name: 报表类型--日报
        :param roleIds: 选择角色id
        :param roles: 全部角色
        :param status:启停状态
        :param remark:备注
        :return:返回新增结果
        '''
        objType=Template().ObjTypeTrans(objType_name)  #坐席转换对象类型成码表
        reportType=Template().IfReportType_doubleChoice(reportType_name)  #判断判断报表类型是否多选，返回转码的报表类型
        rangeId=Template().CodeTrans_rangeId(objType_name,rangeName)   #return:被转换成code的rangeid

        params={"id":"","name":name,"objType":objType,"rangeId":rangeId,"rangeName":rangeName,"remark":remark,
                "reportType":reportType,"roles":roles,"status":status,"roleIds":roleIds
                }
        data=json.dumps(params)
        response = requests.post('http://m-report-test.icsoc.net/api/manager-old-app/reportTemplate/saveReportTemplate',
                                 data=data,cookies=self.cookie,headers=self.header)
        # response = requests.post('http://m-report.icsoc.net/api/manager-old-app/reportTemplate/saveReportTemplate',
        #                          data=data,cookies=self.cookie2,headers=self.header)
        ret = response.json()
        return ret

    def Add_Online_Template(self,name,objType_name,rangeName,reportType_name='半小时明细,半小时叠加,小时明细,小时叠加,日报,月报'
                    ,roleIds='all',roles='全部角色',status=1,remark=''):
        '''新增线上环境模板
        :param name: 模板名称
        :param objType_name: 对象类型--坐席
        :param rangeName: 指标名称
        :param reportType_name: 报表类型--日报
        :param roleIds: 选择角色id
        :param roles: 全部角色
        :param status:启停状态
        :param remark:备注
        :return:返回新增结果
        '''
        objType=Template().ObjTypeTrans(objType_name)  #坐席转换对象类型成码表
        reportType=Template().IfReportType_doubleChoice(reportType_name)  #判断判断报表类型是否多选，返回转码的报表类型
        rangeId=Template().CodeTrans_online_rangeId(objType_name,rangeName)   #return:被转换成code的rangeid

        params={"id":"","name":name,"objType":objType,"rangeId":rangeId,"rangeName":rangeName,"remark":remark,
                "reportType":reportType,"roles":roles,"status":status,"roleIds":roleIds
                }
        data=json.dumps(params)
        response = requests.post('http://m-report.icsoc.net/api/manager-old-app/reportTemplate/saveReportTemplate',
                                 data=data,cookies=self.cookie2,headers=self.header)
        ret = response.json()
        return ret

    def TypeNameTrans(self,reportType_name):
        '''
        :param reportType_name:
        :return: 被转换的报表类型--日报、月报
        '''
        reportType=''
        if reportType_name == '半小时明细':
            reportType = 'PT30M_DETAIL'
        elif reportType_name == '半小时叠加':
            reportType = 'PT30M_ADD'
        elif reportType_name == '小时明细':
            reportType = 'PT1H_DETAIL'
        elif reportType_name == '小时叠加':
            reportType = 'PT1H_ADD'
        elif reportType_name == '日报':
            reportType = 'P1D_DETAIL'
        elif reportType_name == '月报':
            reportType = 'P1M_DETAIL'
        elif reportType_name == '周报':
            reportType = 'P1W_DETAIL'
        return reportType
    def ObjTypeTrans(self,objType_name):
        '''
        :param objType_name:
        :return: 被转换的对象类型--坐席、号码组。。。
        '''
        objType=''
        if objType_name == '坐席':
            objType = "agId"
        elif objType_name == '业务组':
            objType = "grpId"
        elif objType_name == '技能组':
            objType = "callQue"
        elif objType_name == '号码组':
            objType = "serverNum"
        elif objType_name == '呼叫中心':
            objType = "callcenter"
        elif objType_name == '地区':
            objType = "city"
        else:
            print('对象类型输入错误')
        return objType
    def CodeTrans_rangeId(self,obj,rangeName):  #获取指标code
        '''
        :param obj:对象类型--坐席、技能组
        :param rangeName:中文指标字符串
        :return:被转换成code的rangeid
        '''
        params = {'_t':self.t}
        data = json.dumps(params)
        response=requests.post('http://m-report-test.icsoc.net/api/manager-old-app/fieldCode/addTemplateCodeList',
                               cookies=self.cookie,headers=self.header,data = data)
        ret = response.json()
        all_res1=ret['data']['fieldCode']['codeList']
        res1=[]  #中文指标名
        res2=[]  #code
        rangeId=''  #最终传参的rangeid
        test=''
        objtrans=Template().ObjTypeTrans(obj)
        for i in all_res1:
            if objtrans==i['objType']:
                res1.append(i['label'])
                res2.append(i['value'])
                test +=i['label']+','
        # print(test)

        rangeName = rangeName.replace('，', ',')
        rangename_list = rangeName.split(',')  # 获取的所有中文名称
        for i in range(len(res1)):
            for j in rangename_list:
                if j == res1[i]:
                    rangeId += res2[i] + ','
        rangeId = rangeId[:-1]
        return  rangeId

    def CodeTrans_online_rangeId(self,obj,rangeName):  #获取指标code
        '''
        :param obj:对象类型--坐席、技能组
        :param rangeName:中文指标字符串
        :return:被转换成code的rangeid
        '''
        response=requests.post('http://m-report.icsoc.net/api/manager-old-app/fieldCode/addTemplateCodeList',
                               cookies=self.cookie2,headers=self.header)
        ret = response.json()
        all_res1=ret['data']['fieldCode']['codeList']
        res1=[]  #中文指标名
        res2=[]  #code
        rangeId=''  #最终传参的rangeid
        test=''
        objtrans=Template().ObjTypeTrans(obj)
        for i in all_res1:
            if objtrans==i['objType']:
                res1.append(i['label'])
                res2.append(i['value'])
                test +=i['label']+','
        # print(test)

        rangeName = rangeName.replace('，', ',')
        rangename_list = rangeName.split(',')  # 获取的所有中文名称
        for i in range(len(res1)):
            for j in rangename_list:
                if j == res1[i]:
                    rangeId += res2[i] + ','
        rangeId = rangeId[:-1]
        return  rangeId

    def IfReportType_doubleChoice(self,reportType_name):
        '''
        判断报表类型是否多选
        :param reportType_name:报表类型字符串
        :return:报表类型列表
        '''
        reportType=''  #最终传入的报表类型
        if ',' or '，' in reportType_name:  # 报表类型判断是否是多选
            for i in reportType_name.split(','):
                reportType += Template().TypeNameTrans(i) + ','   #报表类型字符串被转换成报表码表
            reportType = reportType[:-1]
        return reportType

    def DeleteReportTemplate(self,template_name):
        '''删除测试企业模板'''
        template_id_ret=PyLib().getReportTemplate_id()['data']['templateList']
        for i in template_id_ret:
            if i['name'] == template_name:
                self.template_id=i['id']
        params={"id":self.template_id}
        data=json.dumps(params)
        response=requests.post('http://m-report-test.icsoc.net/api/manager-old-app/reportTemplate/deleteReportTemplate',
                               data=data,cookies=self.cookie,headers=self.header)
        ret = response.json()
        return ret

    def Delete_Online_ReportTemplate(self, template_name):
        '''删除线上企业模板'''
        template_id_ret = Online_PyLib().getReportTemplate_id()['data']
        for i in template_id_ret:
            if i['name'] == template_name:
                self.template_id = i['id']
        params = {"id": self.template_id}
        data = json.dumps(params)
        response = requests.post('http://m-report.icsoc.net/api/manager-old-app/reportTemplate/deleteReportTemplate',
                                 data=data, cookies=self.cookie2, headers=self.header)
        ret = response.json()
        return ret


if __name__ == '__main__':
    params1_ag='总呼入量,呼入量,坐席呼入量,ACD呼入量,被转接客户量,强拆客户量,内部呼入量,被转接坐席量,' \
            '强拆坐席量,总呼入接通量,呼入接通量,坐席呼入接通量,ACD呼入接通量,被转接客户接通量,内部呼入接通量,被转接坐席接通量' \
            ',强拆坐席接通量,总呼入呼损量,呼入未接通量,坐席呼入未接通量,总呼入通话时长,呼入通话时长,ACD呼入通话时长,' \
            '被转接客户通话时长,内部呼入通话时长,被转接坐席通话时长,强拆坐席通话时长,强拆客户通话时长,外呼量,' \
            '外呼接通量,外呼通话时长,外呼最大通话时长,内部通话时长,内部最大通话时长,呼入转移数,呼出转移数,被三方时长,被三方量,' \
            '置闲次数,总置忙次数,总置忙时长,其他置忙次数,其他置忙时长,置闲时长,总事后整理量,呼入事后整理量,外呼事后整理量,' \
            '呼入事后整理时长,外呼事后整理时长'
    params2_ag='呼入振铃次数,外呼拨打次数,外呼拨打时长,呼入振铃总时长,呼入保持数,外呼保持数,呼入保持时长,' \
               '推送量,外呼保持时长,未推送量,客户挂机未推送量,呼入咨询数,转接未推送量,外呼咨询数,强拆未推送量,呼入咨询时长,' \
               '坐席强退未推送量,外呼咨询时长,坐席挂机未推送量,评价成功量,评价失败量,呼入三方数,评价时长,外呼三方数,未成功评价次数,' \
               '呼入三方时长,满意度评价结果+次数,外呼三方时长,呼入推送量,总登录时长,呼入未推送量,呼入客户挂机未推送量,呼入转接未推送量,' \
               '呼入强拆未推送量,呼入被监听数,呼入被强插数,呼入被强拆数,外呼被监听数,外呼被强插数,外呼被强拆数,被咨询量,被咨询接通量,' \
               '被内部直呼量,被内部直呼接通量,内部直呼通话时长,强拆客户接通量,内部直呼接通量,ACD呼入未接通量,' \
               'ACD呼入未接通量（客户挂机）,ACD呼入未接通量（坐席挂机)'
    params3_ag='被内部直呼通话时长,被咨询时长,内部直呼量,总内部直接通话量,总内部直接通话时长,总转接数,总转移数,内部转移数,' \
               '总振铃次数,总振铃时长,总保持次数,总保持时长,咨询量,咨询时长,三方次数,三方时长,总发起三方次数,总发起三方时长,' \
               '总通话时长,总事后整理时长,总发起咨询次数,总发起咨询时长'
    params_duilie='15秒接听量,20秒接听量,25秒接听量,30秒接听量,5秒呼损量,10秒呼损量,15秒呼损量,20秒呼损量,30秒呼损量,' \
                    '5秒放弃量,10秒放弃量,15秒放弃量,20秒放弃量,30秒放弃量,通话时长,总事后整理时长(接通),' \
                    '最大事后整理时长(接通),首次来电解决量,来电客户量,来电接通客户量,振铃时长,振铃次数,' \
                    '排队时长,总进线量,IVR转队列进线量' \
                    ',其他队列溢出进线量,本队列溢出进线量,坐席转队列进线量,呼损量,满队列溢出量,无坐席溢出量,无效时间溢出量' \
                    ',队列中客户放弃量,超时溢出量,总等待时长,呼损等待时长,满队列溢出等待时长' \
                    ',无效时间溢出等待时长,无坐席溢出等待时长,客户放弃中等待时长,超时溢出等待时长,' \
                    '接听中总等待时长,有效进线量,客户放弃中排队时长,超时溢出排队时长' \
                    ',接听中总排队时长,首接量,接听量,坐席挂机数(接通),客户挂机数(接通),5秒接听量,10秒接听量'

    # params1_city = '呼入量,呼入接通量,呼入通话时长,呼入事后整理时长,外呼量,外呼接通量,外呼通话时长,外呼事后整理时长'

    params1_haomazu='推送量,未推送量,客户挂机未推送量,转接未推送量,强拆未推送量,坐席强退未推送量,坐席挂机未推送量,评价成功量,' \
                    '评价失败量,评价时长,未成功评价次数,满意度评价结果+次数,呼入推送量,呼入未推送量,呼入客户挂机未推送量,' \
                    '呼入转接未推送量,呼入强拆未推送量,呼入坐席强退未推送量,呼入坐席挂机未推送量,呼入评价成功量,呼入评价失败量' \
                    ',呼入评价时长,呼入未成功评价次数,呼入满意度评价结果+次数,外呼推送量,外呼未推送量,外呼客户挂机未推送量,' \
                    '外呼转接未推送量,外呼强拆未推送量,外呼坐席强退未推送量,外呼坐席挂机未推送量,外呼评价成功量,外呼评价失败量,' \
                    '外呼评价时长,外呼未成功评价次数,外呼满意度评价结果+次数'

    params2_haomazu='总进线量,固话来电量,手机来电量,系统未接听数,黑名单来电数,VIP呼入数（白名单）,' \
                    '人工服务请求量,人工服务接听量,人工服务请求量1,人工服务接听量1,中继首次解决量,呼入通话时长,' \
                    '总呼入访问时长,总等待时长,振铃次数,振铃时长,5秒接听量,10秒接听量,15秒接听量,20秒接听量,' \
                    '25秒接听量,30秒接听量,总IVR进线量,中继转IVR进线量,坐席转IVR进线量,IVR挂机量,IVR转队列量,IVR转坐席量,' \
                    'IVR转分机量,IVR转电话量,IVR转留言量,IVR时长,客户放弃中排队时长,超时溢出排队时长,' \
                    '接听中总排队时长,接听坐席人数'


    params1_callcenter='进线量,IVR呼入量,人工服务请求量,人工服务接通量,人工服务请求量1,人工服务接听量1,5秒接听量,10秒接听量' \
                       ',15秒接听量,20秒接听量,25秒接听量,' \
                       '30秒接听量,来电客户量,来电客户接通量,首次解决量,总等待时长,外呼量,外呼接通量,总登录时长,通话时长,' \
                       '呼入通话时长,外呼通话时长,总事后整理时长,呼入事后整理时长,外呼事后整理时长,置闲时长,振铃时长,' \
                       '呼入振铃次数,呼入振铃时长,保持时长,咨询时长,置忙总时长,其他置忙时长,推送量,未推送量,' \
                       '客户挂机未推送量,转接未推送量,强拆未推送量,坐席强退未推送量,坐席挂机未推送量,评价成功量,评价失败量,' \
                       ',客户放弃中排队时长,超时溢出排队时长,接听中总排队时长,应答坐席量'

    params2_callcenter='评价时长,未成功评价次数,呼入推送量,呼入未推送量,呼入客户挂机未推送量,外呼评价时长,外呼未成功评价次数,' \
                       '呼入转接未推送量,呼入强拆未推送量,呼入坐席强退未推送量,呼入坐席挂机未推送量,呼入评价成功量,' \
                       '呼入评价失败量,呼入评价时长,呼入未成功评价次数,外呼推送量,外呼未推送量,' \
                       '外呼客户挂机未推送量,外呼转接未推送量,外呼强拆未推送量,外呼坐席强退未推送量,外呼坐席挂机未推送量,' \
                       '外呼评价成功量,外呼评价失败量,呼入满意度评价结果+次数,满意度评价结果+次数,外呼满意度评价结果+次数'
    all_params=[params1_ag,params2_ag,params3_ag,params_duilie,params1_haomazu,params2_haomazu,params1_callcenter,
                params2_callcenter]
    names=['Auto_坐席1','Auto_坐席2','Auto_坐席3','Auto_技能组','Auto_中继1','Auto_中继2','Auto_呼叫中心1','Auto_呼叫中心2']
    type=['坐席','坐席','坐席','技能组','号码组','号码组','呼叫中心','呼叫中心']

    # for i in range(len(names)):  #删除测试环境8个模板
    #     t2=Template().DeleteReportTemplate(names[i])
    #     print(t2)

    # for i in range(len(names)):  #删除线上环境8个模板
    #     # t=PyLib().getReportTemplate_id(names[i])
    #     t2=Template().Delete_Online_ReportTemplate(names[i])
    #     print(t2)

    # for i in range(len(all_params)):  #新增测试环境8个模板
    #     t=Template().AddTemplate(names[i],type[i],all_params[i])
    #     print(t)

    # for i in range(len(all_params)):  #新增线上环境8个模板
    #     t=Template().Add_Online_Template(names[i],type[i],all_params[i])
    #     print(t)
    #
    # t3 = Template().Add_Online_Template('test_技能组1','技能组',params_duilie)
    # print(t3)
    # t3 = Template().AddTemplate('Auto_地区','地区','呼入量,呼入接通量,呼入通话时长,呼入事后整理时长,外呼量,外呼接通量,外呼通话时长,外呼事后整理时长')
    # print(t3)    #新增地区报表
    # t4 = Template().DeleteReportTemplate('test_技能组1')
    # print(t4)
    # t4 = Online_PyLib().getReportTemplate_id()['data']
    # print(t4)
    # t5 = PyLib().getReportTemplate_id()['data']['templateList']
    # print(t5)
    # t1 = Online_PyLib().getAgReport('2019-01-15', '2019-01-15', 'Auto_技能组', que_name='会员组')
    # print(t1)
