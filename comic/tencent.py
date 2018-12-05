# coding: utf-8

import re
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import urllib.request

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/4.0 (compatible; MSIE 5.5; windows NT)"  )

browser = webdriver.PhantomJS(desired_capabilities=dcap)

#打开动漫的第一页

browser.get("http://ac.qq.com/ComicView/index/id/539443/cid/1")

for i in range(10):
    js = 'window.scrollTo('+str(i*1280)+','+str((i+1)*1280)+')'
    browser.execute_script(js)
    time.sleep(1)

#获取当前页面所有源码（此时包含触发出来的异步加载的资源）

data = browser.page_source

#将相关网页源码写入本地文件中，方便分析

fh=open("D:/Python35/dongman.html","w",encoding="utf-8")
fh.write(data)
fh.close()
browser.quit()

#构造正则表达式提取动漫图片资源网址
pat='<img src="(http:..ac.tc.qq.com.store_file_download.buid=.*?name=.*?).jpg"'
#获取所有动漫图片资源网址

allid=re.compile(pat).findall(data)

for i in range(0,len(allid)):
    #得到当前网址
    thisurl=allid[i]
    #去除网址中的多余元素amp;

    thisurl2=thisurl.replace("amp;","")+".jpg"

    #输出当前爬取的网址
    print(thisurl2)

    #设置将动漫存储到本地的本地目录
    localpath="D:/Python35/dongman/"+str(i)+".jpg"

    #通过urllib对动漫图片资源进行爬取
    urllib.request.urlretrieve(thisurl2,filename=localpath)
