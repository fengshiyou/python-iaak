# -*- coding: UTF-8 -*-
import os
from BaseModel import BaseModel

os.sys.path.append("../config")


class myCollectModel(BaseModel):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(myCollectModel, self).__init__()

        # 创建一个表  只要设置表名  就可以使用基础model中封装的方法 简单的 增删改查
        self.table = "my_collect"
        self.setConCode("SET NAMES utf8mb4;")

