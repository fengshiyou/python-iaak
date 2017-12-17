# -*- coding: UTF-8 -*-
import os

# 获取当前执行该文件的脚本的相对路径
dir = os.path.dirname(__file__)
os.sys.path.append(os.path.join(dir, "../../base"))

from SpiderAction import Action as SpiderAction
class BaseAction(SpiderAction):

    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(BaseAction, self).__init__()

    # def urlOpenError(self):
    #     print "已经重写"
