# -*- coding: UTF-8 -*-
import os
import time
from BaseModel import BaseModel

# 获取当前执行该文件的脚本的相对路径
dir = os.path.dirname(__file__)
os.sys.path.append(os.path.join(dir, "../config"))



class myCollectDayRankModel(BaseModel):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(myCollectDayRankModel, self).__init__()

        # 创建一个表  只要设置表名  就可以使用基础model中封装的方法 简单的 增删改查
        self.table = "my_collect_day_rank"
        self.setConCode("SET NAMES utf8mb4;")

    def makeDayRank(self , day):
        today_timestamp = long(time.mktime(time.strptime(day, '%Y-%m-%d %H:%M:%S')))
        yesterday_timestamp = today_timestamp + 86400
        sql = '''insert into ''' +  self.getTable() + '''
         SELECT
                id,
                plat,
                plat_name,
                liver_id,
                liver_name,
                liver_addr,
                sex,
                country_code,
                country_name,
                avatar,
                online,
                fans,
                plat_currency,
                plat_currency_grow,
                money,
                money_grow,
                @rownum := @rownum + 1 AS money_grow_rank,
                ratio, ''' +  "'" + day+  "'" +  "AS created_at," + str(today_timestamp) + " AS created_at_timestamp," + "'" + day+  "'" +  "AS updated_at," + str(today_timestamp) + " AS updated_at_timestamp" + '''
            FROM
                (
                    SELECT
                        '0' AS id,
                        plat,
                        my_collect.plat_name,
                        liver_id,
                        liver_name,
                        liver_addr,
                        sex,
                        country_code,
                        country_name,
                        avatar,
                        max(ONLINE) AS online,
                        max(fans) AS fans,
                        max(plat_currency) AS plat_currency,
                        max(plat_currency) / ratio AS money,
                        ifnull(
                            (
                                max(plat_currency) - yeaterday_plat_currency
                            ) / ratio,
                            0
                        ) AS plat_currency_grow,
                        ifnull(
                            (
                                max(plat_currency) - yeaterday_plat_currency
                            ) ,
                            0
                        ) AS money_grow,
                        ratio
                    FROM
                        my_collect
                    LEFT JOIN (
                        SELECT
                            liver_id AS tmp_liver_id,
                            plat AS tmp_plat,
                            MAX(plat_currency) AS yeaterday_plat_currency
                        FROM
                            my_collect
                        WHERE
                            created_at_timestamp < ''' + str(today_timestamp) + '''
                        GROUP BY
                            liver_id,
                            plat
                    ) AS tmp ON tmp_liver_id = my_collect.liver_id
                    AND tmp_plat = my_collect.plat
                    LEFT JOIN my_plat ON my_collect.plat = my_plat.plat_id
                    WHERE
                        created_at_timestamp > ''' + str(today_timestamp) + '''
                        and created_at_timestamp < ''' + str(yesterday_timestamp) + '''
                    GROUP BY
                        liver_id,
                        plat
                    ORDER BY
                        plat_currency_grow DESC
                ) AS t,
            (SELECT @rownum := 0) r
    '''

        self._do(sql)
        self.close()

if __name__ == '__main__':
    today = time.strftime('%Y-%m-%d 00:00:00')
    print today
    exit()
    myCollectDayRankModel().makeDayRank("2017-12-17 00:00:00")
