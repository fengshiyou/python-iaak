# -*- coding: UTF-8 -*-
# 设置连接信息，配置，隐藏字段等 以及一些其他的可封装的方法
import os

# 获取当前执行该文件的脚本的相对路径
dir = os.path.dirname(__file__)
os.sys.path.append(os.path.join(dir, "../config"))

# 导入基础配置
import config

# 底层model路径
# 获取当前执行该文件的脚本的相对路径
dir = os.path.dirname(__file__)
os.sys.path.append(os.path.join(dir, "../../base"))

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
