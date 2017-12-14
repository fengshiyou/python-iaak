# -*- coding: UTF-8 -*-
import os
import time
from BaseAction import BaseAction
os.sys.path.append("../model")




class LivemeAction(BaseAction):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(LivemeAction, self).__init__()

        # 城市列表url
        self.country_list_url = "https://live.ksmobile.net/CountryLive/getCountryList"
        self.liver_list_url = "https://live.ksmobile.net/live/featurelist"

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

        if(page_index == 3):
            return all_liver

        # 该页是否有主播数据
        if len(spider_return['video_info']) > 0:
            # 有数据 合并列表
            all_liver.extend(spider_return['video_info'])
            # 页码加1
            page_index = page_index + 1
            # 递归自己
            return self.getAllLiverByCode(country_code, page_index, all_liver)

        else:
            return all_liver


    # 入口 获取主播列表
    def startSaveList(self):
        from myCollectLivemeTmpModel import myCollectLivemeTmpModel
        country_list = self.getCountryList()
        for country in country_list['data']:
            # @todo 拆出一个线程 合并执行获取和保存
            all_liver = self.getAllLiverByCode(country['countryCode'])
            print "do"
            for data in all_liver:
                # 更新时间
                data["updated_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # 更新时间 时间戳
                data["updated_at_timestamp"] = int(time.time())
                # 创建时间
                data["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # 创建时间时间戳
                data["created_at_timestamp"] = int(time.time())
                # 平台id
                data["plat"] = 'liveme'
                # 平台名称
                data["plat_name"] = 'liveme'
                # 主播id
                data["liver_id"] = data['userid']
                # 主播名称
                data["liver_name"] = data['uname']
                # 直播地址
                data["liver_addr"] = 'http://www.liveme.com/live.html?videoid=' + str(data['vid'])
                # 性别 0女1男
                data["sex"] = str(data['sex'])
                # 所在国家编号
                data["area"] = data['area']
                # 所在区域编号
                data["country_code"] = country['countryCode']
                # 主播头像
                data["avatar"] = -1
                # 在线人数
                data["online"] = data['watchnumber']
                # 粉丝数量
                data["fans"] = -1
                # 追随者数量
                data["following_count"] = -1
                # 平台货币
                data["plat_currency"] = -1
                # 国家英文
                data["country_name"] = country['countryName']

            myCollectLivemeTmpModel().add(all_liver)
        myCollectLivemeTmpModel().copyDataToTable("my_collect")
        myCollectLivemeTmpModel().clearTable()

    # 入口 获取主播信息
    def startSaveLiverInfo(self):
        from myCollectModel import myCollectModel
        print myCollectModel().take(1).orderBy("id asc").select()


LivemeAction().startSaveLiverInfo()
