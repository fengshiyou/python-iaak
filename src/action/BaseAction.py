# -*- coding: UTF-8 -*-
import os

os.sys.path.append("../../base")

from SpiderAction import Action as SpiderAction
class BaseAction(SpiderAction):

    def __init__(self):
        # python 2 用super 父类一定要继承object 否则报错
        super(BaseAction, self).__init__()

    # def urlOpenError(self):
    #     print "已经重写"
