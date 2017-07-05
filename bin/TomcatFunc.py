#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from until import FormatPrint
from until import JsonFileFunc
from until import Path
import until
import os
import ConfFunc


class TomcatFunc(object):
    def __init__(self):
        pass

    # 关闭tomcat
    def stopTomcat(self, tomcatScriptPath, tomcatTag=None):
        if "test" == until.env:
            FormatPrint.printDebug("test env ,stopTomcat return True")
            return True
        if not tomcatScriptPath:
            FormatPrint.printError("tomcat stop script path not given")
            return False
        if tomcatTag is None:
            FormatPrint.printError("the stop tomcat tag not given")
            return False
        else:
            FormatPrint.printInfo("will be stopped tomcat tag is :" + str(tomcatTag))
            command = str(tomcatScriptPath) + " -m stop -i " + str(tomcatTag)
            FormatPrint.printDebug("will be executed command is :" + str(command))
            if os.system(command) == 0:
                FormatPrint.printInfo("stop tomcat" + str(tomcatTag) + "success")
                return True
            else:
                FormatPrint.printInfo("stop tomcat" + str(tomcatTag) + "failed")
                return False

    # 启动tomcat
    def startTomcat(self, tomcatScriptPath, tomcatTag=None):
        if "test" == until.env:
            FormatPrint.printDebug("test env ,startTomcat return True")
            return True
        if tomcatScriptPath is None:
            FormatPrint.printError("tomcat start script path not given")
            return False
        if tomcatTag is None:
            FormatPrint.printError("the start tomcat tag not given")
            return False
        else:
            FormatPrint.printInfo("will be started tomcat tag is :" + str(tomcatTag))
            command = str(tomcatScriptPath) + " -m start -i " + str(tomcatTag)
            FormatPrint.printDebug("will be executed command is :" + str(command))
            if os.system(command) == 0:
                FormatPrint.printInfo("start tomcat" + str(tomcatTag) + "success")
                return True
            else:
                FormatPrint.printInfo("start tomcat" + str(tomcatTag) + "failed")
                return False

    # 重启tomcat
    def restartTomcat(self, tomcatScriptPath, tomcatTag=None):
        self.stopTomcat(tomcatScriptPath, tomcatTag)
        self.startTomcat(tomcatScriptPath, tomcatTag)
        FormatPrint.printInfo("restart tomcat " + str(tomcatTag) + " executed , not ensure the process success")
        return True

    # 重启tomcat组
    def restartTomcats(self, tomcatScriptPath, tomcatTags=None):
        for tomcatTag in tomcatTags:
            self.restartTomcat(tomcatScriptPath, tomcatTag)
        FormatPrint.printInfo("restart tomcats finished , not ensure the process success")
        return True

    def restartGroup(self, projectName, group):
        confFuncObj = ConfFunc.getInstance(projectName)
        tags = confFuncObj.getTomcatTagsByGroup(group)
        tomcatScript = confFuncObj.tomcatScript
        result = self.restartTomcats(tomcatScript, tags)
        FormatPrint.printInfo("restart project " + projectName + " " + group + " group tomcats finished , not ensure the process success")
        return result

    # 如果关闭不成功强制关闭
    def killProcessPID(self, tomcatScriptPath, tomcatTag=None):
        if not tomcatScriptPath:
            FormatPrint.printError("tomcat script path not given")
            return False
        if tomcatTag is None:
            FormatPrint.printError("the kill tomcat tag not given")
            return False
        else:
            FormatPrint.printInfo("will be killed tomcat tag is :" + str(tomcatTag))
            command = str(tomcatScriptPath) + " -m killpid -i " + str(tomcatTag)
            FormatPrint.printDebug("will be executed command is :" + str(command))
            if os.system(command) == 0:
                FormatPrint.printInfo("kill tomcatPid" + str(tomcatTag) + "success")
                return True
            else:
                FormatPrint.printInfo("kill tomcatPid" + str(tomcatTag) + "failed")
                return False

    # 获取运行中的tomcat标识
    def getRunningTomcats(self, projectName):
        if projectName is None:
            FormatPrint.printError("get running tomcats not given the project name ")
            return None
        else:
            path = Path.getInstance().runtimeDirPath + str(projectName) + '-node-health-status.json'
            nodeHealthStatusJson = JsonFileFunc.getInstance().readFile(path)
            if nodeHealthStatusJson is None:
                return None
            else:
                return nodeHealthStatusJson['nodeinfo'].keys()


def getInstance():
    return TomcatFunc()
