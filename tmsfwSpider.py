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
from bs4 import BeautifulSoup
import re
# from selenium.webdriver.common.proxy import *


site = 'http://www.howzf.com/esfn/EsfnSearch_csnew.jspx'


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



price_limit_upper = str(230)

area_limit_lower = str(50)


def one_driver_house(driver, area):
    # time = datetime.datetime.now()
    date = datetime.date.today()

    driver.find_element_by_id(area_map[area]).click()
    time.sleep(5)

    # 户型
    # driver.find_element_by_id('ro_2').click()
    # driver.find_element_by_id('ro_3').click()

    # 物业类型
    driver.find_element_by_id('wylx_10').click()
    time.sleep(5)

    # 总价上限
    driver.find_element_by_id('prh').send_keys(price_limit_upper)  # 总价上限
    driver.find_element_by_xpath('//*[@id="search_all"]/div/ul[16]/li[7]/div').click()
    time.sleep(5)  # 控制间隔时间，等待浏览器反映

    # 面积下限
    driver.find_element_by_id('areal').send_keys(area_limit_lower)
    driver.find_element_by_xpath('//*[@id="search_all"]/div/ul[17]/li[7]/div').click()
    time.sleep(5)

    total_page_num = driver.find_element_by_css_selector('font.color-blue09').text

    print('total {} pages'.format(total_page_num))
    total_page_num = int(total_page_num)


    # flag = True
    # page_num = 0
    # results = []
    for page_num in range(1, total_page_num + 1):
        # 保存页面
        # print driver.page_source
        # source_code = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        # source_code = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]').get_attribute("outerHTML")
        source_code = driver.find_element_by_class_name('picNews_list').get_attribute("outerHTML")
        # try:
        #     tmp_results = html_parser(source_code)
        #     results += tmp_results
        # except Exception as e:
        #     print(e)
        print(type(source_code))
        dstdir = './buyHouse/{}/'.format(date)
        if not exists(dstdir):
            makedirs(dstdir)
        f = codecs.open(dstdir + area + '-' + str(page_num) + '.html', 'w+', 'utf8')
        f.write(source_code)
        f.close()

        next_page = None
        try:
            # next_page = driver.find_element_by_id('/html/body/div[5]/div[2]/div[2]/div/ul/div[32]/div/a[10]')
            next_page = driver.find_element_by_link_text('下一页')
        except Exception as e:
            print(e)

        print("page: {}".format(page_num))
        # if next_page:
        try:
            next_page.click()
            time.sleep(2)  # 控制间隔时间，等待浏览器反映
            # page_num += 1
        except Exception as e:
            print('next_page could not be clicked, area is :{} and page is {}'.format(area, page_num+1))
            print(e)
                # flag = False
        # else:
            # flag = False

    # dstdir_merge = './buyHouse'
    # if not exists(dstdir_merge):
    #     makedirs(dstdir_merge)
    # with open(os.path.join(dstdir_merge, area + '.csv'), 'w', encoding='utf-8') as f_w:
    #     for r in results:
    #         f_w.write(r + '\n')


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


def house_worker_no_proxy(area):

    # 用chrome驱动
    chrome_driver = r"D:\Program Files\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver)

    # 用firefox
    # firefox_driver = 'D:\Program Files (x86)\Mozilla Firefox\geckodriver.exe'
    # driver = webdriver.Firefox(executable_path=firefox_driver)
    # driver = webdriver.Firefox()

    driver.get(site)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    driver.refresh()
    # driver.maximize_window()  # 将浏览器最大化显示
    time.sleep(5)  # 控制间隔时间，等待浏览器反映
    # num = len(areas_list)
    # for i in range(num):
    #     # if city == areas_list[i]:
    #     #     continue
    #     # from_city = city
    #     area = areas_list[i]
    #     one_driver_ticket(driver, area)
    one_driver_house(driver, area)
    # one_driver_ticket(driver, area)
    driver.close()


def html_parser(html):
    soup = BeautifulSoup(html, "lxml")

    # 获得有小区信息的panel
    house_elements = soup.find_all('div', class_="houseBox2 borderBottom")
    results = []
    for house_elem in house_elements:
        title = house_elem.find('a', class_='fl w480')

        title_text = title.text.strip()

        xiaoqu = title_text.split(' ')[0]

        url = title.get('href', 'null')

        if url == 'null':
            pass
        else:
            url = 'http://www.howzf.com' + url

        info_lines = house_elem.find_all('div', class_='house_listinfo_line f14')

        district, desc = 'null', 'null'
        for info in info_lines:
            if info.find(name='a'):
                district = info.text.strip()
            else:
                desc = info.text.strip()

        district = re.sub('[\r\n]', '', district)
        desc = re.sub('[\r\n]', '', desc)

        # year = 'null'

        year = desc.split('|')[-1].strip('')
        year = re.sub('建成', '', year)

        price = house_elem.find('div', class_="house_price_total")

        price = price.find('strong').text.strip()

        if int(price) < int(price_limit_upper):
            if year == 'null' or int(year) > 1999:
                result = [district, xiaoqu, title_text, price, desc, year, url]
                string_r = ','.join(result)
                results.append(string_r)

    return results


# def all_ticket_no_proxy():
#     pool = mp.Pool(processes=1)
#     pool.map(ticket_worker_no_proxy, areas_list)  # map(f, [x1, x2, x3, x4]) = [f(x1), f(x2), f(x3), f(x4)]
#     pool.close()
#     pool.join()

def get_areas(areas):
    for area in areas:
        house_worker_no_proxy(area)


if __name__ == '__main__':
    print("start")
    start = datetime.datetime.now()
    # all_ticket_proxy() # proxy
    # all_ticket_no_proxy() # no proxy
    # areas_list = ['上城', '下城', '江干', '拱墅', '西湖', '滨江', '之江', '下沙', '萧山', '余杭']
    areas_list = ['拱墅']
    get_areas(areas_list)
    end = datetime.datetime.now()
    print("end")
    print("time: ", end-start)
