import pandas as pd

import json
from urllib.request import urlopen, quote
import requests


def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'j8oq8dtVx2FP9hRLlB8gguVCi30K1yUN'  # 百度地图ak，具体申请自行百度，提醒需要在“控制台”-“设置”-“启动服务”-“正逆地理编码”，启动
    # EdjWGv3caPLjuh1II4LQNWaMglwNmlNg
    address = quote(address)  # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
    # print(uri)
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    try:
        lat = temp['result']['location']['lat']
        lng = temp['result']['location']['lng']
    except:
        # print(address)
        return
    return lat, lng   # 纬度 latitude, 经度 longitude


data = pd.read_csv('E:\PycharmProjects\lianjia-beike-spider\data\lianjia\ershou\hz\\20191027\\all.csv')
# data

for indexs in data.index:
    addr = data.loc[indexs, '小区']
    get_location = getlnglat(addr)
    if get_location:
        get_lat = get_location[0]
        get_lng = get_location[1]
    else:
        print(addr)
        get_lat, get_lng = 'null', 'null'
    data.loc[indexs, '纬度'] = get_lat
    data.loc[indexs, '经度'] = get_lng

# data

# data_html = pd.DataFrame(columns=['content'])

data_html = []

for indexs in data.index:
    if data.loc[indexs, '纬度'] == 'null' or data.loc[indexs,'经度'] == 'null':
        pass
    else:
        # data_html.loc[indexs,'content'] = '{' + \
        #                                   '"lat":' + str(data.loc[indexs,'纬度']) + ',' +  \
        #                                   '"lng":' + str(data.loc[indexs,'经度']) + ',' +  \
        #                                   '"quyu":' + '"' + str(data.loc[indexs,'小区']) +'"' +   \
        #                                   '}' + ','

        data_html.append('{' + \
                         '"lat":' + str(data.loc[indexs,'纬度']) + ',' +  \
                        '"lng":' + str(data.loc[indexs,'经度']) + ',' +  \
                        '"quyu":' + '"' + str(data.loc[indexs,'小区']) +'"' +   \
                        '}' )

# data_html.to_csv("data_html.csv",encoding="gbk")
# data_html

with open("data_html.csv", 'w', encoding="gbk") as f_html:
    for data in data_html:
        f_html.write(data + ',\n')

