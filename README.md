## 网络爬虫之Selenium使用代理登陆：爬取[透明售房网二手房](http://www.howzf.com/esfn/EsfnSearch_csnew.jspx)网站 

**一些说明：**
* python3

* 使用selenium模拟浏览器登陆，获取相关html。

* 代理可以存入一个文件，程序读取并使用。

* 支持多进程抓取。


### 1 安装相应python包
 cmd命令行输入:
 
`pip install -r requirements.txt`

### 2 驱动可选择chorme或者firefox
#### (1)安装chrome浏览器驱动（这里是在windows上开发的, 需安装Chrome)
 下载地址: https://sites.google.com/a/chromium.org/chromedriver/home
 
 下载完成后运行.exe文件
 
 将exe文件添加到环境变量Path
 ####(2)安装Firefox浏览器驱动(未成功，TODO)
 下载地址:https://github.com/mozilla/geckodriver/releases
 
 解压后放到firefox安装路径下面


### 3 运行爬虫程序

 `python tmsfwSpider.py`
 
 运行结果自动保存在当前路径下
