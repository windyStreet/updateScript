#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from until import FormatPrint
import TomcatFunc
import ConfFunc
import NginxFunc
import CheckService
import RunningFunc
import NodeRunStatusFunc
import os


# ProjectFunc 项目功能，必须保证基本运行文件存在的情况下才可以生效

class ProjectFunc(object):
    def __init__(self, projectName):
        self.projectName = projectName
        self.tomcatFuncObj = TomcatFunc.getInstance()
        self.confFuncObj = ConfFunc.getInstance(self.projectName)
        self.nginxFuncObj = NginxFunc.getInstance(self.projectName)
        self.nodeRunStatusFuncObj = NodeRunStatusFunc.getInstance(self.projectName)
        self.checkServiceObj = CheckService.getInstance(self.projectName)
        pass

    # 关闭项目
    def stopProject(self):
        runningTomcatTags = TomcatFunc.getInstance().getRunningTomcats(self.projectName)
        if runningTomcatTags is None:
            FormatPrint.printInfo("can not get the running tomcats info,please check the config or running the project first")
        else:
            tomcatScript = self.nodeRunStatusFuncObj.getNodeRunStatusInfo()['tomcatScript']
            for tomcatTag in runningTomcatTags:
                TomcatFunc.getInstance().stopTomcat(tomcatScript,tomcatTag)

    # 启动项目
    def startProject(self):
        runningTomcatTags = TomcatFunc.getInstance().getRunningTomcats(self.projectName)
        if runningTomcatTags is None:
            FormatPrint.printInfo("can not get the running tomcats info,please check the config or running the project first")
        else:
            tomcatScript = self.nodeRunStatusFuncObj.getNodeRunStatusInfo()['tomcatScript']
            for tomcatTag in runningTomcatTags:
                TomcatFunc.getInstance().startTomcat(tomcatScript,tomcatTag)

    # 重启项目
    def restartProject(self):
        FormatPrint.printInfo(self.projectName + " restart start")
        nodeStatusInfo = NodeRunStatusFunc.getInstance(self.projectName).getNodeRunStatusInfo()
        tomcatScript = nodeStatusInfo['tomcatScript']
        if nodeStatusInfo is not None:
            keyInfos = nodeStatusInfo['nodeinfo']
            keys = keyInfos.keys()
            length = len(keys)
            if length < 1:
                FormatPrint.printInfo("to restart project " + self.projectName + " only one tomcat , restart it")
                # 重启tomcat
                TomcatFunc.getInstance().restartTomcats(tomcatScript, keys)
                # 检查tomcat是否已经重启成功
                successTomcatTags = CheckService.getInstance(self.projectName).getSuccessRestartTomcatTags(keys)
                if len(successTomcatTags) > 0:
                    FormatPrint.printInfo(self.projectName + " project " + str(successTomcatTags) + " tomcat had restart success")
                else:
                    FormatPrint.printWarn(self.projectName + " no tomcat restart success")
            else:
                keys1 = []
                keys2 = []
                for i in range(length):
                    if i < length / 2:
                        keys1.append(keys[i])
                    else:
                        keys2.append(keys[i])
                #######################################################################################################################
                FormatPrint.printInfo(self.projectName + " modify NG , del " + str(keys1))
                NginxFunc.getInstance(self.projectName).changeNginxConf(keys2)
                FormatPrint.printInfo(self.projectName + " restart tomcat " + str(keys1) + " start")
                TomcatFunc.getInstance().restartTomcats(tomcatScript, keys1)
                successTomcatTags1 = CheckService.getInstance(self.projectName).getSuccessRestartTomcatTags(keys1)
                if len(successTomcatTags1) > 0:
                    FormatPrint.printInfo(self.projectName + " project tomcat " + str(successTomcatTags1) + " had restart success")
                else:
                    FormatPrint.printWarn(self.projectName + " no tomcat restart success")
                #######################################################################################################################
                FormatPrint.printInfo(self.projectName + " modify NG , del " + str(keys2))  # 不理解为啥执行完了，这个keys1就空了，难道是在getSuccessRestartTomcatTags方法中被删除了
                NginxFunc.getInstance(self.projectName).changeNginxConf(successTomcatTags1)
                FormatPrint.printInfo(self.projectName + " restart tomcat " + str(keys2) + " start")
                TomcatFunc.getInstance().restartTomcats(tomcatScript, keys2)

                successTomcatTags2 = CheckService.getInstance(self.projectName).getSuccessRestartTomcatTags(keys2)
                if len(successTomcatTags2) > 0:
                    FormatPrint.printInfo(self.projectName + " project tomcat " + str(successTomcatTags2) + " had restart success")
                else:
                    FormatPrint.printWarn(self.projectName + " no tomcat restart success")
                #######################################################################################################################
                FormatPrint.printInfo(self.projectName + " modify NG , add " + str(keys))
                NginxFunc.getInstance(self.projectName).changeNginxConf(successTomcatTags1 + successTomcatTags2)
        else:
            FormatPrint.printError(self.projectName + " nodeStatusInfo is None")

        FormatPrint.printInfo("restart project:" + self.projectName + " finish")
        pass

    # 更新项目
    def updateProject(self):
        if "single" == self.confFuncObj.deploymentMode:
            return self.__singleUpdateProject__(),  # 独立模式
        if "onehalf" == self.confFuncObj.deploymentMode:
            return self.__onehalfUpdateProject__(),  # 分布模式
        if "double" == self.confFuncObj.deploymentMode:
            return self.__doubleUpdateProject__(),  # 双组模式
        FormatPrint.printFalat(self.confFuncObj.hostStr + " updateProject get wrong deployment mode")

    # 更新项目 独立模式
    def __singleUpdateProject__(self):
        # 初始化 node health 文件
        if self.nodeRunStatusFuncObj.initNodeHealthStatus():
            FormatPrint.printInfo(self.confFuncObj.hostStr + " init node-health-status file success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " init node-health-status file failed")

        # 重启某组的 tomcat
        groups = RunningFunc.getInstance(self.projectName).getWillUpdateGroups(self.confFuncObj.deploymentMode)
        if self.tomcatFuncObj.restartGroup(self.projectName, groups[0]):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " restart masterGroup success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " restart masterGroup failed")

        # 检查tomcat是否已经重启完成
        successTomcatTags = self.checkServiceObj.getSuccessUpdateTomcatTags(groups[0])
        if len(successTomcatTags) > 0:
            FormatPrint.printInfo(self.confFuncObj.hostStr + " get the success restart tomcat is " + str(successTomcatTags))
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " get the success restart tomcat failed")

        # 修改NG配置文件
        if self.nginxFuncObj.changeNginxConf(successTomcatTags):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " modify NG success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " modify NG failed")

        FormatPrint.printInfo(self.confFuncObj.hostStr + " __singleUpdateProject__ finished")

    # 更新项目 分布模式 (先更新 backupGroup )
    def __onehalfUpdateProject__(self):
        # 初始化 node health 文件
        if self.nodeRunStatusFuncObj.initNodeHealthStatus():
            FormatPrint.printInfo(self.confFuncObj.hostStr + " init node-health-status file success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " init node-health-status file failed")

        # 修改nginx的信息,修改nginx的配置信息，保证在更新过程中的upstream可用
        inUpstreamTomcatTags_1 = self.confFuncObj.getTomcatTagsByGroup("masterGroup")
        if self.nginxFuncObj.changeNginxConf(inUpstreamTomcatTags_1):  # 修改NG的配置
            FormatPrint.printInfo(self.confFuncObj.hostStr + " modify NG at befor update to ensure the project running success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " modify NG at befor update to ensure the project running failed")

        # 重启将要被更新的组的信息
        if self.tomcatFuncObj.restartGroup(self.projectName, "backupGroup"):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " restart backupGroup tomcat success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " restart backupGroup tomcat failed")

        # 检查服务是否可用
        successTomcatTags_1 = self.checkServiceObj.getSuccessUpdateTomcatTags("backupGroup")
        if len(successTomcatTags_1) > 0:
            FormatPrint.printInfo(self.confFuncObj.hostStr + " check backupGroup tomcat services is OK success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " check backupGroup tomcat services is OK success")

        # 重新设置NG配置 == 》 第一组跟新完毕,同时进行了切换
        if self.nginxFuncObj.changeNginxConf(successTomcatTags_1):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " backupGroup tomcat restart success , modify NG to ensure the masterGroup update and project running , success ")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " backupGroup tomcat restart success , modify NG to ensure the masterGroup update and project running , failed")

        # 重启第二组 重启将要被更新的组的信息
        if self.tomcatFuncObj.restartGroup(self.projectName, "masterGroup"):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " restart masterGroup tomcat success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " restart masterGroup tomcat success")

        # 检查服务是否可用
        successTomcatTags_2 = self.checkServiceObj.getSuccessUpdateTomcatTags("masterGroup")
        if len(successTomcatTags_2) > 0:
            FormatPrint.printInfo(self.confFuncObj.hostStr + " check masterGroup tomcat services is OK success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " check masterGroup tomcat services is OK success")

        # 重置ng配置文件
        if self.nginxFuncObj.changeNginxConf(successTomcatTags_1 + successTomcatTags_2):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " tomcat restart success , modify NG to ensure project running , success ")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " tomcat restart success , modify NG to ensure project running , success ")

        FormatPrint.printInfo(self.confFuncObj.hostStr + " __onehalfUpdateProject__ finished")
        pass

    # 更新项目 多组模式
    def __doubleUpdateProject__(self):
        # 初始化 node health 文件
        if self.nodeRunStatusFuncObj.initNodeHealthStatus():
            FormatPrint.printInfo(self.confFuncObj.hostStr + " init node-health-status file success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " init node-health-status file failed")

        # 重启某组的 tomcat
        groups = RunningFunc.getInstance(self.projectName).getWillUpdateGroups(self.confFuncObj.deploymentMode)
        if self.tomcatFuncObj.restartGroup(self.projectName, groups[0]):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " restart masterGroup success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " restart masterGroup failed")

        # 检查tomcat是否已经重启完成
        successTomcatTags = self.checkServiceObj.getSuccessUpdateTomcatTags(groups[0])
        if len(successTomcatTags) > 0:
            FormatPrint.printInfo(self.confFuncObj.hostStr + " get the success restart tomcat is " + str(successTomcatTags))
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " get the success restart tomcat failed")

        # 修改NG配置文件
        if self.nginxFuncObj.changeNginxConf(successTomcatTags):
            FormatPrint.printInfo(self.confFuncObj.hostStr + " modify NG success")
        else:
            FormatPrint.printFalat(self.confFuncObj.hostStr + " modify NG failed")

        FormatPrint.printInfo(self.confFuncObj.hostStr + " __doubleUpdateProject__ finished")
        pass

    # 替换项目资源 (使用平台方式,可以通过读取上传的更新信息来获取更新时间以及更新版本)
    def replaceProjectResource(self, updateVersion=None,updateTime=None):
        if updateTime is None or updateVersion is None:
            updateTime = RunningFunc.getInstance(self.projectName).getUpdateTime()
            updateVersion = RunningFunc.getInstance(self.projectName).getUpdateVersion()

        if updateTime is None or updateVersion is None:
            FormatPrint.printFalat(self.confFuncObj.hostStr + "replace project resource not get the right update info ")

        command = self.confFuncObj.tomcatScript + " -m replaceResource -p " + self.projectName + " -t " + updateTime + " -v" + updateVersion
        FormatPrint.printInfo("exec project resource replace command:" + str(command))
        if os.system(command) == 0:
            FormatPrint.printInfo(self.confFuncObj.hostStr + " replace resource success ")
            return True
        else:
            FormatPrint.printInfo(self.confFuncObj.hostStr + " replace resource failed ")
            return False

    # 切换项目
    def exchangeProject(self):
        pass


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get ProjectFunc Object , not given projectName")
    return ProjectFunc(projectName)

