# -*- coding: UTF-8 -*-
import MySQLdb
import os
import time, re


class model(object):
    def __init__(self, params):
        ##params 数据库配置###
        self.db_host = params['db_host']
        self.db_user = params['db_user']
        self.db_passwd = params['db_passwd']
        self.db_db = params['db_db']
        self.db_charset = params['db_charset']

        # 默认连接方式
        self.con_code = "SET NAMES utf8"
        # 默认查询字段
        self.query_find = "*"
        # 默认查询条件
        self.query_where = 1
        # 插入时没有数据的默认值
        self.add_default_value = ""

############################### 核心 可封装 ###############################

    # 设置table
    def setTable(self, table):
        self.table = table

    # 获取table名称
    def getTable(self):
        return self.table

    # 数据库连接
    def connectDb(self):
        try:
            self._connect = MySQLdb.connect(
                host=self.db_host,
                user=self.db_user,
                passwd=self.db_passwd,
                db=self.db_db,
                charset=self.db_charset)
            # 初始化连接编码 SET NAMES utf8

        except MySQLdb.Error, e:
            self.error = e.args
            self.connectError()
        self._cursor = self._connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.setConCode(self.con_code)




    # 设置连接编码
    def setConCode(self, code):
        # todo 坑爹的东西 有空整理   创建连接以后，游标对象首先要执行一遍“SET NAMES utf8mb4;”这样就能保证数据库连接是以utf8mb4编码格式连接，数据库也就变成utf8mb4的啦
        self._cursor.execute(code)

############################### 核心 可封装 结束 ###############################


############################### 查询构建器 可封装 ###############################

################ 查询构建器 连贯操作 中间部分 ################
    # @todo 连贯操作,左联待实现
    def leftJoin(self):
        1

    # 连贯操作,组装要查询的字段名
    def find(self, *fields):
        query_find = ''
        for field in fields:
            query_find = query_find + str(field) + ","
        self.query_find = query_find[:-1]
        return self

    # 连贯操作,组装查询条件 where
    def where(self, fields, tmp, value):
        if (self.query_where != 1):
            self.query_where = self.query_where + " AND " + fields + " " + tmp + " " + str(value)
        else:
            self.query_where = fields + " " + tmp + " " + str(value)
        return self

    # 连贯操作,组装查询条件 orwhere
    def orwhere(self, fields, tmp, value):
        if (self.query_where != 1):
            self.query_where = self.query_where + " OR " + fields + " " + tmp + " " + str(value)
        else:
            self.query_where = fields + " " + tmp + " " + str(value)
        return self

################ 查询构建器 连贯操作 中间部分 结束 ################

################ 查询构建器 连贯操作 收尾动作 ################
    # 插入数据
    def add(self, data_list):

        # 获取列名
        columus = self.getColumu()
        # insert_list 待插入数据列表
        insert_list = list()

        # 组装带插入数据列表
        for data in data_list:
            # 判断类型 强制要求data_list中必须是字典
            if (type(data) != dict):
                raise Exception("更新的数据类型必须是dict")

            # 待插入数据
            insert_data = list()
            # 遍历字段列表
            for columu in columus:
                # 字段名
                key = columu['COLUMN_NAME']
                # 如果是自增id
                if (key == 'id'):
                    insert_data.append(0)
                else:
                    # 判断数据中是否存在要插入的列
                    if key in data:
                        insert_data.append(data[key])
                    else:
                        # 没有要插入的列，则该列插入默认字段
                        insert_data.append(self.add_default_value)
            # 数据组装
            insert_list.append(insert_data)
        # sql插入字段变量模板
        value_tmp = ''

        # 待插入的第一个列表作为标准
        for i in range(len(insert_list[0])):
            # 组装 sql插入字段变量模板
            value_tmp = value_tmp + "%s,"

        # 生成sql语句
        insert_sql = "insert into " + self.getTable() + " VALUES ("
        insert_sql = insert_sql + value_tmp[:-1]
        insert_sql = insert_sql + ")"

        # 判断原始数据列表长度，决定执行sql时是否循环执行
        if(len(data_list) == 1):
            self._do(insert_sql, insert_list[0], 1)
            return self._connect.insert_id()
        else:
            self._do(insert_sql, insert_list, 0)
            return True

    # 获取列信息
    def getColumu(self):

        column_select = "select COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '" + self.getTable() + "'"
        self._do(column_select)
        return self.rows2array(self._cursor.fetchall())

    # 根据连贯操作设置 where find等信息进行查询
    def select(self):
        # @todo order by ,group by,limit m,n  等连贯操作待实现
        sql = "SELECT " + self.query_find + " FROM " + self.getTable() + " WHERE " + str(self.query_where)

        if(self._do(sql)):
            result = self.rows2array(self._cursor.fetchall())
            # 如果结果长度为1,则直接返回结果集
            if len(result) == 1:
                return result[0]
            # 返回结果数组
            return result
        else:
            return False
    def rows2array(self, data):
        # '''transfer tuple to array.'''
        result = []
        for da in data:
            if type(da) is not dict:
                raise Exception('Format Error: data is not a dict.')
            result.append(da)
        return result


    # 更新操作
    def update(self, data_dict):

        # 判断是否生成where查询条件
        if (self.query_where == 1):
            raise Exception("没有where条件")
        # 待更新数据必须是字典
        if (type(data_dict) != dict):
            raise Exception("更新的数据类型必须是dict")
        # 组装update sql 中的set语句
        update_set = ' SET '
        for key in data_dict:
            update_set = update_set + str(key) + " = '" + str(data_dict[key]) + "',"
        # 最终sql
        sql = "UPDATE " + self.getTable() + update_set[:-1] + " WHERE " + self.query_where

        if(self._do(sql)):
            return True
        else:
            return False

    # 执行sql
    # type：0多条 1一条
    # data sql中的变量数据
    def _do(self, sql, data='', type=1):
        self.connectDb()
        try:
            if (type == 1):
                self._cursor.execute(sql, data)
                self._connect.commit()
            else:
                self._cursor.executemany(sql, data)
                self._connect.commit()
            return True
        except MySQLdb.Error, e:
            self.error = e.args
            self.doError()

################ 查询构建器 连贯操作 收尾动作 结束 ################

############################### 异常相关 ###############################
    # mysql连接时的错误信息 捕获到的错误信息，具体处理方法由子类重写
    def connectError(self):
        time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print time
        # @todo 向上传递异常待补充 抛出异常，子类可以重写
        raise Exception("数据库连接错误，错误信息记录在self.error中。子类重写“connectError方法来处理或记录”")
    # 执行sql语句时的错误信息 捕获到的错误信息，具体处理方法由子类重写
    def doError(self):
        time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print time
        # @todo 向上传递异常待补充 抛出异常，子类可以重写
        raise Exception("数据库连接错误，错误信息记录在self.error中。子类重写“connectError方法来处理或记录”")
############################### 异常结束 ###############################
