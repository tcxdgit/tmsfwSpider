#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import datetime
import codecs
import multiprocessing as mp
from os import makedirs
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.proxy import *


# site = 'http://flight.qunar.com'
site = 'http://www.howzf.com/esfn/EsfnSearch_csnew.jspx'
# site = ''
# hot_city_list = [u'上海', u'北京', u'广州', u'深圳']
# num = len(hot_city_list)


"""
<li id="aid_p">
		<a href="#" onclick="doArea('')" class="f_red">不限</a>
				    		<a href="#" onclick="doArea('330102')" id="area_330102">上城</a>
		    		<a href="#" onclick="doArea('330103')" id="area_330103">下城</a>
		    		<a href="#" onclick="doArea('330104')" id="area_330104">江干</a>
		    		<a href="#" onclick="doArea('330105')" id="area_330105">拱墅</a>
		    		<a href="#" onclick="doArea('330106')" id="area_330106">西湖</a>
		    		<a href="#" onclick="doArea('330108')" id="area_330108">滨江</a>
		    		<a href="#" onclick="doArea('330110')" id="area_330110">之江</a>
		    		<a href="#" onclick="doArea('330186')" id="area_330186">下沙</a>
		    		<a href="#" onclick="doArea('330231')" id="area_330231">大江东</a>
		    		<a href="#" onclick="doArea('330181')" id="area_330181">萧山</a>
		    		<a href="#" onclick="doArea('330184')" id="area_330184">余杭</a>
		    		<a href="#" onclick="doArea('330187')" id="area_330187">富阳</a>
		    		<a href="#" onclick="doArea('330399')" id="area_330399">杭州周边</a>
	</li>
"""

area_map = {"上城": "area_330102",
            "下城": "area_330103",
            "江干": "area_330104",
            "拱墅": "area_330105",
            "西湖": "area_330106",
            "滨江": "area_330108",
            "之江": "area_330110",
            "下沙": "area_330186",
            "大江东": "area_330231",
            "萧山": "area_330181",
            "余杭": "area_330184",
            "富阳": "area_330187",
            "杭州周边": "area_330399"
            }


room_map = {"一室": "ro_1",
            "二室": "ro_2",
            "三室": "ro_3",
            "四室": "ro_4",
            "四室及以上": "ro_5"}

wylx_map = {"住宅": "wylx_10",
            "非住宅": "wylx_20"}

# //*[@id="prh"]

# /html/body/div[4]/div[2]/div/div/ul[16]/li[5]/input

areas_list = ['上城', '下城', '江干', '拱墅', '西湖', '滨江', '之江', '下沙', '萧山', '余杭']


def one_driver_ticket(driver, area):
    # time = datetime.datetime.now()
    date = datetime.date.today()
    # tomorrow = date+datetime.timedelta(days=1)
    # date格式转为string格式
    # tomorrow_string = tomorrow.strftime('%Y-%m-%d')

    # driver.find_element_by_name('fromCity').clear()
    # driver.find_element_by_name('fromCity').send_keys(from_city)
    # driver.find_element_by_name('toCity').clear()
    # driver.find_element_by_name('toCity').send_keys(to_city)
    # driver.find_element_by_name('fromDate').clear()
    # driver.find_element_by_name('fromDate').send_keys(tomorrow_string)
    # driver.find_element_by_xpath('//button[@type="submit"]').click()
    # driver.find_element_by_id('aid_p')
    # username = driver.find_element_by_xpath("//li[@id='aid_p']/input[1]")


    # driver.find_element_by_xpath('//*[@id="area_330102"]')
    driver.find_element_by_id(area_map[area]).click()
    time.sleep(5)

    # 户型
    # driver.find_element_by_id('ro_2').click()
    # driver.find_element_by_id('ro_3').click()

    # 物业类型
    driver.find_element_by_id('wylx_10').click()
    time.sleep(5)

    # 总价
    # driver.find_element_by_id('pr_0_100').click()
    # driver.find_element_by_id('pr_100_150').click()
    # driver.find_element_by_id('pr_150_200').click()
    # driver.find_element_by_id('pr_200_300').click()
    # driver.find_element_by_id('ro_3')

    # driver.find_element_by_xpath('//*[@id="prh"]').send_keys('250')
    driver.find_element_by_id('prh').send_keys('250')
    driver.find_element_by_xpath('//*[@id="search_all"]/div/ul[16]/li[7]/div').click()
    # driver.find_element_by_class_name('queding ml10 CP').click()
    driver.find_element_by_css_selector('')
    time.sleep(5)  # 控制间隔时间，等待浏览器反映

    flag = True
    page_num = 0
    while flag:
        # 保存页面
        # print driver.page_source
        # source_code = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        # source_code = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]').get_attribute("outerHTML")
        source_code = driver.find_element_by_class_name('picNews_list').get_attribute("outerHTML")
        print(type(source_code))
        dstdir = './buyHouse/{}/'.format(date)
        if not exists(dstdir):
            makedirs(dstdir)
        f = codecs.open(dstdir + area + '-' + str(page_num+1) + '.html', 'w+', 'utf8')
        f.write(source_code)
        f.close()

        next_page = None
        try:
            # next_page = driver.find_element_by_id('/html/body/div[5]/div[2]/div[2]/div/ul/div[32]/div/a[10]')
            next_page = driver.find_element_by_link_text('下一页')
        except Exception as e:
            print(e)
            pass
        print("page: %d" % (page_num+1))
        if next_page:
            try:
                next_page.click()
                time.sleep(2)  # 控制间隔时间，等待浏览器反映
                page_num += 1
            except Exception as e:
                print('next_page could not be clicked')
                print(e)
                flag = False
        else:
            flag = False

def get_proxy_list(file_path):
    proxy_list = []
    try:
        f = open(file_path, 'r')
        all_lines = f.readlines() # readlines()每次按行读取整个文件内容，将读取到的内容放到一个列表中，返回list类型。
        for line in all_lines:
            proxy_list.append(line.replace('\r', '').replace('\n', ''))
        f.close()
    except Exception as e:
        print(e)
    return proxy_list
"""
def ticket_worker_proxy(city_proxy):
    city = city_proxy.split(',')[0]
    proxy = city_proxy.split(',')[1]
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxy,
        'ftpProxy': proxy,
        'sslProxy': proxy,
        'noProxy': '' # 过滤不需要代理的地址
    })
    driver = webdriver.Firefox(proxy=proxy)
    driver.get(site)
    driver.maximize_window() # 将浏览器最大化显示
    for i in range(num):
        if city == hot_city_list[i]:
            continue
        from_city = city
        to_city = hot_city_list[i]
        one_driver_ticket(driver, from_city, to_city)
    driver.close()

def all_ticket_proxy():
    hot_city_proxy_list = []
    proxy_list = get_proxy_list('./proxy/proxy.txt') # ./表示当前目录，../表示上一级目录
    for i in range(num):
        hot_city_proxy_list.append(hot_city_list[i]+','+proxy_list[i])
    pool = mp.Pool(processes=1)
    pool.map(ticket_worker_proxy, hot_city_proxy_list) # map(f, [x1, x2, x3, x4]) = [f(x1), f(x2), f(x3), f(x4)]
    pool.close()
    pool.join()
"""


def ticket_worker_no_proxy(area):
    chrome_driver = r"D:\Program Files\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver)
    # chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    # os.environ['webdriver.chrome.driver'] = chromedriver
    # driver = webdriver.Chrome(chromedriver)
    driver.get(site)
    time.sleep(10)
    driver.refresh()
    time.sleep(5)
    driver.refresh()
    driver.maximize_window()  # 将浏览器最大化显示
    time.sleep(10)  # 控制间隔时间，等待浏览器反映
    # num = len(areas_list)
    # for i in range(num):
    #     # if city == areas_list[i]:
    #     #     continue
    #     # from_city = city
    #     area = areas_list[i]
    #     one_driver_ticket(driver, area)
    one_driver_ticket(driver, area)
    # one_driver_ticket(driver, area)
    driver.close()


def all_ticket_no_proxy():
    pool = mp.Pool(processes=1)
    pool.map(ticket_worker_no_proxy, areas_list)  # map(f, [x1, x2, x3, x4]) = [f(x1), f(x2), f(x3), f(x4)]
    pool.close()
    pool.join()


if __name__ == '__main__':
    print("start")
    start = datetime.datetime.now()
    # all_ticket_proxy() # proxy
    all_ticket_no_proxy() # no proxy
    end = datetime.datetime.now()
    print("end")
    print("time: ", end-start)
