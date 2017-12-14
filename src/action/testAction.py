# -*- coding: UTF-8 -*-
from BaseAction import BaseAction


class LivemeAction(BaseAction):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(LivemeAction, self).__init__()

        # 城市列表url
        self.country_list_url = "***"
        self.liver_list_url = "***"

    # 获取城市列表
    def getCountryList(self):
        # 设置爬虫url
        self.setSpiderUrl(self.country_list_url)
        return self.getJson()

    # 获取主播列表 递归获取，直到没数据
    def getAllLiverByCode(self,country_code, page_index = 1, all_liver=list()):
        spider_url = self.liver_list_url + "?page_index=" + str(page_index) + "&page_size=20&countryCode=" + country_code

        # 设置爬虫url
        self.setSpiderUrl(spider_url)
        spider_return = self.getJson()['data']

        # 该页是否有主播数据
        if len(spider_return['video_info']) > 0:
            # 有数据 合并列表
            all_liver.extend(spider_return['video_info'])
            # 页码加1
            page_index = page_index + 1
            # 递归自己
            self.getAllLiverByCode(country_code, page_index, all_liver)

        else:
            return all_liver


    # 入口
    def start(self):
        country_list = self.getCountryList()
        for country in country_list['data']:
            # @todo 拆出一个线程 合并执行获取和保存
            all_liver = self.getAllLiverByCode(country['countryCode'])



LivemeAction().start()
