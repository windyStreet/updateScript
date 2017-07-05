#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from until import Path
from until import JsonFileFunc
from until import FormatPrint


class RunningFunc(object):
    def __init__(self, projectName):
        self.projectName = projectName
        pass

    # 获取将要被更新的组
    def getWillUpdateGroups(self, deploymentMode):
        if "single" == deploymentMode:
            return self.__getWillUpdateGroups_single__()  # 独立模式
        if "onehalf" == deploymentMode:
            return self.__getWillUpdateGroups_onehalf__()  # 分布模式
        if "double" == deploymentMode:
            return self.__getWillUpdateGroups_double__()  # 双组模式
        FormatPrint.printFalat(self.confFuncObj.hostStr + " get update group info not given the right deployment mode:" + str(deploymentMode))

    # 获取将要被更新组 独立模式
    def __getWillUpdateGroups_single__(self):
        willUpdateGroups = []
        willUpdateGroups.append("masterGroup")
        return willUpdateGroups

    # 获取将要被更新组 分布模式
    def __getWillUpdateGroups_onehalf__(self):
        willUpdateGroups = []
        willUpdateGroups.append("masterGroup")
        willUpdateGroups.append("backupGroup")
        return willUpdateGroups

    # 获取将要被更新组 双组模式
    def __getWillUpdateGroups_double__(self):
        willUpdateGroups = []
        currentRunGroup = self.getCurrentRunGroup()[0]
        if currentRunGroup == "masterGroup":
            willUpdateGroups.append("backupGroup")
        elif currentRunGroup == "backupGroup":
            willUpdateGroups.append("masterGroup")
        return willUpdateGroups

    # 获取正在运行的组 默认情况下，我们定义masterGroup处于运行状态
    def getCurrentRunGroup(self):
        runGroup = []
        path = Path.getInstance().runtimeDirPath + str(self.projectName) + '-node-health-status.json'
        nodeHealthStatus = JsonFileFunc.getInstance().readFile(path)
        if nodeHealthStatus is None:
            runGroup.append("masterGroup")
            return runGroup
        else:
            return nodeHealthStatus["currentRunGroups"]

    # 获取更新信息
    def getUpdateInfo(self):
        path = Path.getInstance().filesDirPath + 'updateInfo.json'
        updateInfos = JsonFileFunc.getInstance().readFile(path)
        if updateInfos is not None and updateInfos[self.projectName] is not None:
            return updateInfos[self.projectName]

        else:
            FormatPrint.printFalat("can not get right update info")
            return None

    # 获取更新时间
    def getUpdateTime(self):
        updateInfo = self.getUpdateInfo()
        if self.getUpdateInfo() is not None:
            return updateInfo['updateTime']
        else:
            return None

    # 获取更新版本
    def getUpdateVersion(self):
        updateInfo = self.getUpdateInfo()
        if self.getUpdateInfo() is not None:
            return updateInfo['updateVersion']

    # 获取更新内容
    def getUpdateMsg(self):
        updateInfo = self.getUpdateInfo()
        if self.getUpdateInfo() is not None:
            return updateInfo['updateMsg']


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get RunningFunc Object , not given projectName")
    return RunningFunc(projectName)
