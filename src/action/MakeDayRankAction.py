# -*- coding: UTF-8 -*-
import os
import time

from BaseAction import BaseAction

# 获取当前执行该文件的脚本的相对路径
dir = os.path.dirname(__file__)
os.sys.path.append(os.path.join(dir, "../model"))

class MakeDayRankAction(BaseAction):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(MakeDayRankAction, self).__init__()

    def start(self , today=''):
        from myCollectDayRankModel import myCollectDayRankModel
        if(today ==''):
            today = time.strftime('%Y-%m-%d 00:00:00')

        myCollectDayRankModel().makeDayRank(today)

if __name__ == '__main__':
    # MakeDayRankAction().start()
    day_list = [
        '2017-12-10 00:00:00',
        '2017-12-11 00:00:00',
        '2017-12-12 00:00:00',
        '2017-12-13 00:00:00',
        '2017-12-14 00:00:00',
        '2017-12-15 00:00:00',
        '2017-12-16 00:00:00',
        '2017-12-17 00:00:00',
    ]
    for day in day_list:
        MakeDayRankAction().start(day)