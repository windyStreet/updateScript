#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from until import FormatPrint
import NodeRunStatusFunc
import RunningFunc
import TomcatFunc
import ConfFunc
import socket
import time
import urllib2
import json


class CheckService(object):
    def __init__(self, projectName):
        self.projectName = projectName
        self.confFuncObj = ConfFunc.getInstance(self.projectName)  # 配置文件
        self.nodeRunStatus = NodeRunStatusFunc.getInstance(self.projectName).getNodeRunStatusInfo()  # 获取nodeRunStatus信息
        pass

    # 获取重启成功的tomcatTags
    def getSuccessRestartTomcatTags(self, tomcatTags):
        checkTomcatTags = tomcatTags
        return self.getIsOKTomcats(checkTomcatTags)

    # 获取服务是正常的tomcatTags
    def getIsOKTomcats(self, checkTomcatTags):
        hostStr = self.confFuncObj.hostStr
        tomcatRestartMaxTime = self.confFuncObj.tomcatRestartMaxTime  # tomcat最大重启时间
        updateConsumeMaxTime = self.confFuncObj.updateConsumeMaxTime  # 项目更新花费最大时间
        tomcatScript = self.confFuncObj.tomcatScript

        socket.setdefaulttimeout(5)
        sucessRestartTomcattags = []
        tomcatStartTime = time.time()

        while True:
            intervalTime = time.time() - tomcatStartTime
            FormatPrint.printInfo("tomcat restart,service check consume time is :" + str(intervalTime))
            if len(checkTomcatTags) == 0 or (intervalTime > float(tomcatRestartMaxTime) and len(sucessRestartTomcattags) > 0):
                for tomcatTag in sucessRestartTomcattags:
                    FormatPrint.printInfo("tomcat " + str(tomcatTag) + "start success")
                # 记得关闭未启动成功的tocmat
                if len(checkTomcatTags) > 0:
                    for failTomcatTag in checkTomcatTags:
                        TomcatFunc.killTomcat(tomcatScript, failTomcatTag)
                break
            if intervalTime > float(updateConsumeMaxTime):
                FormatPrint.printFalat("IN THN MAX UPDATE TIME , UNABLE TO START ANY TOMCAT , UPDATE PROCESS END")
                return sucessRestartTomcattags
            deltomcatTags = []
            for tomcatTag in checkTomcatTags:
                checkUrl = self.nodeRunStatus['nodeinfo'][tomcatTag]['health-check-url']
                checkPar = self.nodeRunStatus['nodeinfo'][tomcatTag]['health-check-data']
                try:
                    response = urllib2.urlopen(checkUrl, checkPar)
                    ret_data = response.read()
                    ret_code = response.code
                    response.close()
                    if isinstance(ret_data, bytes):
                        ret_data = bytes.decode(ret_data)
                    ret_data = json.loads(ret_data)
                    if ret_data["status"] == 1 and ret_code == 200:
                        FormatPrint.printInfo("####################################################################")
                        FormatPrint.printInfo("tomcat update recording:")
                        FormatPrint.printInfo(str(hostStr) + " , tomcat" + str(tomcatTag) + " update success")
                        FormatPrint.printInfo("tomcat " + str(tomcatTag) + " update start time:" + str(tomcatStartTime))
                        FormatPrint.printInfo("tomcat " + str(tomcatTag) + " update ned time:" + time.strftime('%Y-%m-%d %H:%M:%S'))
                        FormatPrint.printInfo("####################################################################")
                        sucessRestartTomcattags.append(tomcatTag)
                        deltomcatTags.append(tomcatTag)
                except Exception as e:
                    FormatPrint.printWarn(
                        str(hostStr) + ",tomcat" + str(tomcatTag) + " update expection:" + str(e))
            if (len(deltomcatTags) > 0):
                for deltag in deltomcatTags:
                    checkTomcatTags.remove(deltag)
                    # del checkTomcatTags[deltag]
            time.sleep(3)
            # 清空deltomcatTags 临时变量
            del deltomcatTags[:]
        return sucessRestartTomcattags

    # 检查当前服务是否可用（不给出组,默认检查，node文件中的配置）
    def getSuccessUpdateTomcatTags(self, checkGroup=None):
        checkGroups = []
        if checkGroup is None:
            checkGroups = RunningFunc.getInstance(self.projectName).getWillUpdateGroups(self.confFuncObj.deploymentMode)
        else:
            checkGroups.append(checkGroup)
        restartTomcats = self.confFuncObj.getTomcatsByGroups(checkGroups)  # 获取将要重启的Tomcats信息
        checkTomcatTags = []
        for tomcatInfo in restartTomcats:
            checkTomcatTags.append(tomcatInfo['tag'])
        return self.getIsOKTomcats(checkTomcatTags)


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get CheckService Object , not given projectName")
    return CheckService(projectName)
