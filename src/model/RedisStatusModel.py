# -*- coding: UTF-8 -*-
import os
from BaseModel import BaseModel

# 获取当前执行该文件的脚本的相对路径
dir = os.path.dirname(__file__)
os.sys.path.append(os.path.join(dir, "../config"))


class RedisStatusModel(BaseModel):
    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(RedisStatusModel, self).__init__()

        # 创建一个表  只要设置表名  就可以使用基础model中封装的方法 简单的 增删改查
        self.table = "redis_status"

