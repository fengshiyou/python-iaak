# -*- coding: UTF-8 -*-
import urllib
# 导入拓展包开始
import urllib2
from bs4 import BeautifulSoup
import time
import json

class Action(object):
    def __init__(self):
        # 爬虫地址
        self.spider_url = ""
        # 爬虫请求头
        self.spider_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        # 爬虫 post 表单
        self.spider_post_data = ""
        # 爬虫请求时间
        self.spider_time_out = 60
        # 文本读取编码
        self.spider_read_type = "utf-8"
        # 返回值类型 html json
        self.spider_return_type = "html"
        # 属性是否被继承测试
        self.test="test"

    def sysPathAppend(self, package):
        import os
        os.sys.path.append(package)

    def setSpiderUrl(self, url):
        self.spider_url = url

    def setSpiderHeader(self, header):
        self.spider_header = header

    def setSpiderPostData(self, post_data):
        self.spider_post_data = post_data

    def setSpiderTimeOut(self, time_out):
        self.spider_time_out = time_out

    def setSpiderReadType(self, read_type):
        self.spider_read_type = read_type

    def setSpiderReturnType(self, return_type):
        self.spider_return_type = return_type

    def getHtml(self):
        return self.spiderReturn()

    def getJson(self):

        self.setSpiderReturnType('json')
        spider_return = self.spiderReturn()
        if not spider_return:
            return False
        else:
            return json.loads(spider_return)

    def spiderReturn(self):
        url = self.spider_url

        # post数据
        if (self.spider_post_data == ''):
            request = urllib2.Request(url=url, headers=self.spider_header)
        else:
            data = urllib.urlencode(post_data)
            request = urllib2.Request(url=url, data=data, headers=self.spider_header)
        try:
            response = urllib2.urlopen(request, timeout=self.spider_time_out)
            html_doc = response.read().decode(self.spider_read_type)

            if (self.spider_return_type=="html"):
                soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf8')
                return soup
            else:
                return html_doc
        except:
            self.urlOpenError()

    def urlOpenError(self):
        print "url打开错误，由子类重写处理方式(记录错误数据？等等)"