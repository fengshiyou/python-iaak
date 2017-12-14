# -*- coding: UTF-8 -*-
import os
from BaseModel import BaseModel
os.sys.path.append("../config")

class test(BaseModel):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(test, self).__init__()

        # 创建一个表  只要设置表名  就可以使用基础model中封装的方法 简单的 增删改查
        self.table = "test"

    def makeTestTable(self):
        make_table_sql = '''CREATE TABLE `''' + self.table + '''` (
                     `id` int(11) NOT NULL AUTO_INCREMENT,
                     `liver_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '直播平台对应的主播id',
                     `liver_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '主播名字',
                     PRIMARY KEY (`id`),
                     KEY `liver_id` (`liver_id`)
                   ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测试表';'''
        self._do(make_table_sql)

    def testAddMor(self):
        self.add([{"liver_id": 222,"liver_name":"222name"}, {"liver_id": 333,"liver_name":"333name"},{"liver_id": 444,"liver_name":"444name"}])

    def testAddOne(self):
        self.add([{"liver_id": 111,"liver_name":"111name"}])

    def testGetOne(self):
        print self.find('liver_id', 'liver_name').where("liver_id", "=", 222).select()
    def testGetMor(self):
        print self.find('liver_id', 'liver_name').where("liver_id", ">", 222).orwhere("liver_id", "=", 111).select()

    def testUpdate(self):
        self.where("liver_id", "=", 222).orwhere("liver_id", "=", 333).update({"liver_name": "被更改过"})

if __name__ == '__main__':

    test().makeTestTable() # 创建测试表
    # test().testAddMor() # 增加多条数据
    # test().testAddOne() # 增加一条数据
    # test().testGetOne() # 获取一条数据
    # test().testGetMor() # 获取多条数据
    # test().testUpdate() # 更新数据