# -*- coding: UTF-8 -*-
import os
from BaseModel import BaseModel

os.sys.path.append("../config")


class myCollectLivemeTmpModel(BaseModel):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(myCollectLivemeTmpModel, self).__init__()

        # 创建一个表  只要设置表名  就可以使用基础model中封装的方法 简单的 增删改查
        self.table = "my_collect_liveme_tmp"
        self.setConCode("SET NAMES utf8mb4;")

    def copyDataToTable(self, to_table):
        insert_into_sql = '''
            INSERT INTO ''' + to_table + ''' SELECT
                '0' AS id,
                plat,
                plat_name,
                liver_id,
                liver_name,
                liver_addr,
                sex,
                area,
                '-1' AS country_code,
                '-1' AS country_name,
                '-1' AS avatar,
                max(ONLINE) AS ONLINE,
                '-1' AS fans,
                '-1' AS following_count,
                '-1' AS plat_currency,
                max(created_at) AS created_at,
                max(created_at_timestamp) AS created_at_timestamp,
                max(updated_at) AS updated_at,
                max(updated_at_timestamp) AS updated_at_timestamp
            FROM
                ''' + self.getTable() + '''
            GROUP BY
                liver_id
        '''
        self._do(insert_into_sql)
        self.close()
