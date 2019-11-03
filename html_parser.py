from bs4 import BeautifulSoup
import os
import re

price_limit_upper = 215

def html_parser(html):
    soup = BeautifulSoup(html, "lxml")

    # 获得有小区信息的panel
    house_elements = soup.find_all('div', class_="houseBox2 borderBottom")
    # house_elements = soup.find_all(name='div', attrs={'class': 'house_listinfo ml20', 'style': 'width:450px;'})
    results = []
    for house_elem in house_elements:
        try:
            title = house_elem.find('a', class_='fl w480')

            title_text = title.text.strip()

            xiaoqu = title_text.split(' ')[0]

            url = title.get('href', 'null')

            if url == 'null':
                pass
            else:
                url = 'http://www.howzf.com' + url

            info_lines = house_elem.find_all('div', class_='house_listinfo_line f14')

            location, desc = 'null', 'null'
            for info in info_lines:
                if info.find(name='a'):
                    location = info.text.strip()
                else:
                    desc = info.text.strip()

            location = re.sub('[\r\n]', '', location)
            desc = re.sub('[\r\n]', '', desc)

            # if location == 'null':
            #     district, area = 'null', 'null'
            # else:
            if location == 'null':
                district, area = 'null', 'null'
            else:
                district, area = location.split(' ')
                district = district.strip('[')
                # area = area.strip(']')
                area = re.sub(r'\].*', '', area)

            year = desc.split('|')[-1].strip('')
            year = re.sub('建成', '', year)

            _house_size = re.findall('面积(.*)㎡', title_text)
            room_num = re.findall('.室.*厅.*卫', title_text)
            room_num = re.sub(' ', '', room_num[0])

            if _house_size:
                house_size = _house_size[0]
            else:
                house_size = 'null'

            price = house_elem.find('div', class_="house_price_total")

            price = price.find('strong').text.strip()

            if int(price) < int(price_limit_upper):
                if year == 'null' or int(year) > 1999:
                    result = [district, area, xiaoqu, price, desc, year, house_size, room_num, url]
                    string_r = ','.join(result)
                    results.append(string_r)
        except AttributeError:
            continue
    return results


def parser(html_dir):
    results = []
    for html_file in os.listdir(html_dir):
        if html_file.endswith('.html'):
            html = open(os.path.join(html_dir, html_file), 'r', encoding='utf-8')
            results_page = html_parser(html)
            results += results_page

    with open(os.path.join(html_dir, 'all_tmsfw.csv'), 'w', encoding='utf_8_sig') as f_csv:
        f_csv.write('区域,版块,小区,总价(万起),描述,年份,面积(㎡), 户型, url\n')

        for r in results:
            f_csv.write(r + '\n')


if __name__ == "__main__":
    parser('.\\buyHouse\\2019-11-03')

