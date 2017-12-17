# -*- coding: UTF-8 -*-
import os
import time

from BaseAction import BaseAction



# 获取当前执行该文件的脚本的相对路径
dir = os.path.dirname(__file__)
os.sys.path.append(os.path.join(dir, "../model"))

class RcshowAction(BaseAction):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(RcshowAction, self).__init__()


        self.liver_list_url = "http://rcshow.tv/index.php?c=newHome&a=getSingerData&pagesize=10000&page=1&_r=0.9509398940848115"
        self.liver_info_url = "http://rcshow.tv/live/"
        self.liver_info_sex_url = "http://rcshow.tv/?c=user&a=getInfoCard&uid="




    def getAllLiver(self):

        spider_url = self.liver_list_url

        # 设置爬虫url
        self.setSpiderUrl(spider_url)
        spider_return = self.getJson()
        return spider_return


    def getLiverInfo(self, skip, take):
        import re
        from myCollectModel import myCollectModel


        no_fans_list = myCollectModel().skip(skip).take(take).orderBy("id desc").where("fans", "=", -1).where("plat","=","rcshow").select()
        for no_fans_liver in no_fans_list:

            url = no_fans_liver['liver_addr']

            # 因为多个线程同时跑  所以不能用self   因为改变了返回值形式
            rcshow_thread = RcshowAction()
            rcshow_thread.setSpiderUrl(url)

            doc_soup = rcshow_thread.getHtml()

            plat_currency_doc = doc_soup.find_all(attrs={"class": "c-weight"})

            plat_currency = plat_currency_doc[0].get_text()

            sex_url = rcshow_thread.liver_info_sex_url + str(no_fans_liver['liver_id'])
            rcshow_thread.setSpiderUrl(sex_url)
            sex = rcshow_thread.getJson()['baseInfo']['sex']


            fans_re = re.compile(r"\"fans\":(\d+)")

            fans = fans_re.findall(doc_soup.script.string)[0]

            update_data = dict()

            if (plat_currency.find('t') != -1):
                plat_currency = int(float(plat_currency.replace('t', '')) * 1000 * 1000)
            elif (plat_currency.find('kg') != -1):
                plat_currency = int(float(plat_currency.replace('kg', '')) * 1000)
            elif (plat_currency.find('g') != -1):
                plat_currency = int(plat_currency.replace('g', ''))

            update_data['fans'] = fans
            update_data['plat_currency'] = plat_currency
            update_data['sex'] = sex

            # 更新时间
            update_data['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 更新时间戳
            update_data['updated_at_timestamp'] = int(time.time())

            #
            myCollectModel().where("id","=",no_fans_liver['id']).update(update_data)

    # 入口 获取主播列表
    def startSaveList(self):

        from myCollectModel import myCollectModel
        all_liver = self.getAllLiver()

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
            data["plat"] = 'rcshow'
            # 平台名称
            data["plat_name"] = 'rcshow'
            # 主播id
            data["liver_id"] = data['uid']
            # 主播名称
            data["liver_name"] = data['nick']
            # 直播地址
            data["liver_addr"] = self.liver_info_url + str(data['account'])
            # 性别 0女1男
            data["sex"] = 0
            # 所在国家编号
            data["area"] = -1
            # 所在区域编号
            data["country_code"] = "TW"
            # 主播头像
            data["avatar"] = data['img']
            # 在线人数
            data["online"] = data['people']
            # 粉丝数量
            data["fans"] = -1
            # 追随者数量
            data["following_count"] = -1
            # 平台货币
            data["plat_currency"] = -1
            # 国家英文
            data["country_name"] =  "TaiWan"

        myCollectModel().add(all_liver)

    # 入口 获取主播信息
    def startSaveLiverInfo(self):
        import thread
        import threading

        from RedisStatusModel import RedisStatusModel

        thread_status = RedisStatusModel().where("redis_key", "=", "rcshow_thread_status").select()['redis_val']
        if (thread_status == 0):
            get_num = 100
            RedisStatusModel().where("redis_key", "=", "rcshow_thread_status").update({"redis_val": 1})
            # @todo 封装being完善进程相关
            for i in range(5):
                tmp = threading.Thread(target=self.getLiverInfo, args=(i*get_num,get_num))
                tmp.start()

            while (len(threading.enumerate()) > 1):
                1

            RedisStatusModel().where("redis_key", "=", "rcshow_thread_status").update({"redis_val":0})

if __name__ == '__main__':

    # RcshowAction().startSaveList()
    # RcshowAction().getLiverInfo(0,10000)
    RcshowAction().startSaveLiverInfo()
