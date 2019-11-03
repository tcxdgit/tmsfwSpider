#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import datetime
import codecs
from os import makedirs
from os.path import exists
from selenium import webdriver
from bs4 import BeautifulSoup
import re


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

price_limit_upper = str(230)

area_limit_lower = str(50)
js = "var q=document.body.scrollTop=10000"  # documentElement表示获取body节点元素


def one_driver_house(driver, area):
    # time = datetime.datetime.now()
    date = datetime.date.today()

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
            time.sleep(5)

            # 点击下一页
            next_page.click()
            time.sleep(5)  # 控制间隔时间，等待浏览器反映
        except Exception as e:
            print('next_page could not be clicked, area is :{} and page is {}'.format(area, page_num+1))
            print(e)


def one_driver_new_house(driver):
    # time = datetime.datetime.now()
    date = datetime.date.today()

    # driver.find_element_by_id(area_map[area]).click()
    # time.sleep(5)

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
            time.sleep(10)

            # 点击下一页
            next_page.click()
            time.sleep(10)  # 控制间隔时间，等待浏览器反映
        except Exception as e:
            print('next_page could not be clicked, area is :{} and page is {}'.format(area, page_num+1))
            print(e)


def house_worker_no_proxy(area, new_house=False):

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
    if new_house:
        pass
    else:
        one_driver_house(driver, area)
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


def get_areas(areas):
    for area in areas:
        house_worker_no_proxy(area)


if __name__ == '__main__':
    print("start")
    start = datetime.datetime.now()
    # all_ticket_proxy() # proxy
    # all_ticket_no_proxy() # no proxy
    # areas_list = ['上城', '下城', '江干', '拱墅', '西湖', '滨江', '之江', '下沙', '萧山', '余杭']
    areas_list = ['余杭']
    get_areas(areas_list)
    end = datetime.datetime.now()
    print("end")
    print("time: ", end-start)
