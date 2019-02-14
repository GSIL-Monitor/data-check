#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import pprint

'''查询号码归属地，并且计算省份的各指标数量'''


with open(r'C:\Users\Administrator\Desktop\usernum.txt','r',encoding='utf-8') as f:
    num = f.readlines()

all_num = [] #号码
num_dict={}  #号码：号码的个数

for line in num:
    all_num.append(line.strip())
print(all_num)

#如果all_num[0]不在dict里面，就加进去，并且value+1;否则只+1
for i in all_num:
    if i not in num_dict:
        num_dict[i] = 1
    else:
        a = num_dict[i]
        a +=1
        num_dict[i] = a
print(num_dict)
# print(num_dict.keys())
# print(num_dict.values())
print('电话号码有多少：',len(num_dict))
url = "http://172.31.0.93:8080/search"
# province = {}  #省份：城市
city = {}  #城市：城市里的电话数
#如果num_dict.keys[0]get后的省份不在city里面，就加进去，并且Value+num_dict.values[0]#否则只Value+num_dict.values[0]

for key,value in num_dict.items():
    # if i not in province:
    querystring = {"tel": key}
    response = requests.get(url, params=querystring)
    res = response.json()
    # print(res['province'],res['city'],key)
    # sf = res['province']
    city_name = res['city']
    # if res['province'] not in province:
    #     province[sf] = cs
    if city_name ==None or city_name == '':
        # city['其他'] = value
        city_name ='其他'
    # else:
    if city_name not in city:
        city[city_name] =value
    else:
        a = city[city_name]
        a += value
        city[city_name] = a
pprint.pprint(city)

# print(province)



