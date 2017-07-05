#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os
import time
import until
from until import FormatPrint
from until import Path
import NodesHealthCheck
import NginxUpstreamCheck

global checkCount
checkCount = 0


class HealthCheck(object):
    def __init__(self, projectName):
        self.projectName = projectName

    # 保持检查服务
    def checkServiceAllTime(self):
        while True:
            global checkCount
            checkCount = checkCount + 1
            FormatPrint.printInfo("check " + self.projectName + " project service runing " + str(checkCount) + " times")
            self.checkServiceOnce()
            time.sleep(until.defaultCheckRate)

    # 检查服务单独执行一次
    def checkServiceOnce(self):
        NodesHealthCheck.getInstance(self.projectName).checkNodeService()
        NginxUpstreamCheck.getInstance(self.projectName).checkUpstream()
        return True

    # 启动健康检查
    def startHealthCheck(self):
        path = Path.getInstance().scriptsDirPath + 'healthCheck.sh'
        cmd = path + " start " + self.projectName
        FormatPrint.printInfo("cmd will be exec:" + str(cmd))
        if os.system(cmd) == 0:
            FormatPrint.printInfo("start health check service success")
            return True
        else:
            FormatPrint.printInfo("start health check service failed")
            return False

    # 关闭健康检查
    def stopHealthCheck(self):
        path = Path.getInstance().scriptsDirPath + 'healthCheck.sh'
        cmd = path + " stop " + self.projectName
        FormatPrint.printInfo("cmd will be exec:" + str(cmd))
        if os.system(cmd) == 0:
            FormatPrint.printInfo("stop health check service success ")
            return True
        else:
            FormatPrint.printInfo("stop health check service  failed ")
            return False

    # 重启健康检查
    def restartHealthCheck(self):
        path = Path.getInstance().scriptsDirPath + 'healthCheck.sh '
        cmd = path + " restart " + self.projectName
        FormatPrint.printInfo("cmd will be exec:"+str(cmd))
        if os.system(cmd) == 0:
            FormatPrint.printInfo(" start health check service success ")
            return True
        else:
            FormatPrint.printInfo(" start health check service failed ")
            return False

    # 健康检查服务状态
    def getHealthCheckStatus(self):
        path = Path.getInstance().scriptsDirPath + 'healthCheck.sh'
        cmd = path + " status " + self.projectName
        #os.system(cmd)
        FormatPrint.printInfo("cmd will be exec:" + str(cmd))
        return os.popen(cmd)


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get HealthCheck Object , not given projectName")
    return HealthCheck(projectName)
