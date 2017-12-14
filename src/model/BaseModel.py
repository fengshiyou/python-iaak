# -*- coding: UTF-8 -*-
# 设置连接信息，配置，隐藏字段等 以及一些其他的可封装的方法
import os
# 基础配置路径
os.sys.path.append("../config")
# 导入基础配置
import config

# 底层model路径
os.sys.path.append("../../base")
# 导入底层model
from model import model

# 数据库配置
db_config = dict()
db_config['db_host'] = config.get_conf('db_host')
db_config['db_user'] = config.get_conf('db_user')
db_config['db_passwd'] = config.get_conf('db_passwd')
db_config['db_db'] = config.get_conf('db_db')
db_config['db_charset'] = config.get_conf('db_charset')

class BaseModel(model):
    def __init__(self):

        # python 2 用super 父类一定要继承object 否则报错
        super(BaseModel, self).__init__(db_config)
