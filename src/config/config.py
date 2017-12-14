# -*- coding: UTF-8 -*-
app_env = 'local'

# 数据库配置开始

###local###
# 环境_dbnum_type
local_db_host = '127.0.0.1'
local_db_user = 'root'
local_db_passwd = 'Ace__7'
local_db_db = 'collect'
local_db_charset = 'utf8'

###dev###
dev_db_host = 'rdsfgn76t366iqux8bs3.mysql.rds.aliyuncs.com'
dev_db_user = 'app_admin'
dev_db_passwd = 'appAdmin'
dev_db_db = 'app_12thman'
dev_db_charset = 'utf8'

###pro###
pro_db_host = 'rm-2ze8y15206utgg508o.mysql.rds.aliyuncs.com'
pro_db_user = 'fengshiyou'
pro_db_passwd = '1l95Bd&C1&6Y^iKW'
pro_db_db = 'app_python'
pro_db_charset = 'utf8'

# 自定义包的路径
package_pach = ""


def get_conf(env_name):
    return eval(app_env + "_" + env_name)