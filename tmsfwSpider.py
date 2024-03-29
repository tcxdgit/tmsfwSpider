#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import datetime
import codecs
from os import makedirs
from os.path import exists
from selenium import webdriver
import random

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

"""
room_map = {"一室": "ro_1",
            "二室": "ro_2",
            "三室": "ro_3",
            "四室": "ro_4",
            "四室及以上": "ro_5"}

wylx_map = {"住宅": "wylx_10",
            "非住宅": "wylx_20"}
"""

# 总价上限
price_limit_upper = str(220)

# 面积下限
area_limit_lower = str(50)
js = "var q=document.body.scrollTop=10000"  # documentElement表示获取body节点元素


def one_driver_house(driver, area):
    # time = datetime.datetime.now()
    date = datetime.date.today()

    # 选择区域
    driver.find_element_by_id(area_map[area]).click()
    time.sleep(5)

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

    for page_num in range(1, total_page_num + 1):
        # 保存页面
        if page_num % 36 == 0:
            time.sleep(20)
        source_code = driver.find_element_by_class_name('picNews_list').get_attribute("outerHTML")
        print(type(source_code))
        dstdir = './buyHouse/{}/'.format(date)
        if not exists(dstdir):
            makedirs(dstdir)
        f = codecs.open(dstdir + area + '-' + str(page_num) + '.html', 'w+', 'utf8')
        f.write(source_code)
        f.close()

        next_page = None
        try:
            next_page = driver.find_element_by_link_text('下一页')
        except Exception as e:
            print(e)

        print("page: {}".format(page_num))
        try:
            # 滑动滚动条
            driver.execute_script(js)
            # time.sleep(15)

            sleep_time = random.randrange(10, 20)
            time.sleep(sleep_time)

            # 点击下一页
            next_page.click()
            time.sleep(5)  # 控制间隔时间，等待浏览器反映
        except Exception as e:
            print('next_page could not be clicked, area is :{} and page is {}'.format(area, page_num+1))
            print(e)
            driver.refresh()

        sleep_time = random.randrange(10, 20)
        time.sleep(sleep_time)


def one_driver_new_house(driver, area):
    # time = datetime.datetime.now()
    date = datetime.date.today()

    # 选择区域
    driver.find_element_by_id(area_map[area]).click()
    time.sleep(5)

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

    # 新上房源
    driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div[2]/div[3]/span/input').click()
    time.sleep(5)

    total_page_num = driver.find_element_by_css_selector('font.color-blue09').text

    print('total {} pages'.format(total_page_num))
    total_page_num = int(total_page_num)

    for page_num in range(1, total_page_num + 1):
        # 保存页面
        source_code = driver.find_element_by_class_name('picNews_list').get_attribute("outerHTML")
        print(type(source_code))
        dstdir = './buyHouse/{}/'.format(date)
        if not exists(dstdir):
            makedirs(dstdir)
        f = codecs.open(dstdir + '新上房源-' + str(page_num) + '.html', 'w+', 'utf8')
        f.write(source_code)
        f.close()

        next_page = None
        try:
            next_page = driver.find_element_by_link_text('下一页')
        except Exception as e:
            print(e)

        print("page: {}".format(page_num))
        try:
            # 滑动滚动条
            driver.execute_script(js)
            sleep_time = random.randrange(10, 20)
            time.sleep(sleep_time)

            # 点击下一页
            next_page.click()
            time.sleep(10)  # 控制间隔时间，等待浏览器反映
        except Exception as e:
            print('next_page could not be clicked, page is {}'.format(page_num+1))
            print(e)

        time.sleep(5)


def house_worker_no_proxy(area, only_new_house):

    # 用chrome驱动
    chrome_driver = r"D:\Program Files\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver)

    # TODO: 用firefox
    # firefox_driver = 'D:\Program Files (x86)\Mozilla Firefox\geckodriver.exe'
    # driver = webdriver.Firefox(executable_path=firefox_driver)
    # driver = webdriver.Firefox()

    driver.get(site)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    driver.refresh()
    driver.maximize_window()  # 将浏览器最大化显示
    driver.refresh()

    time.sleep(5)  # 控制间隔时间，等待浏览器反映
    if only_new_house:
        one_driver_new_house(driver, area)
    else:
        one_driver_house(driver, area)

    driver.close()


def get_areas(areas, only_new_house=False):
    """
    :param areas: 要爬取的区域
    :param only_new_house: 是否只看新上房源
    :return:
    """
    print("start")
    start = datetime.datetime.now()
    for area in areas:
        house_worker_no_proxy(area, only_new_house=only_new_house)

    end = datetime.datetime.now()
    print("end")
    print("time: ", end-start)


if __name__ == '__main__':
    # areas_list = ['上城', '下城', '江干', '拱墅', '西湖', '滨江', '之江', '下沙', '萧山', '余杭']
    areas_list = ['萧山']
    get_areas(areas_list)
