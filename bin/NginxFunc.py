#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from until import FormatPrint
from until import Path
from until import JsonFileFunc
import os
import sys
import time
import until


class NginxFunc(object):
    def __init__(self, projectName):
        self.projectName = projectName
        pass

    # 重载nginx
    def reloadNginx(self, cmd):
        FormatPrint.printInfo("exec command:" + str(cmd))
        if "test" == until.env:
            FormatPrint.printDebug("test env ,return True")
            return True
        if os.system(cmd) == 0:
            FormatPrint.printInfo("reload nginx success")
            return True
        else:
            FormatPrint.printError("reload nginx failed ")
            return False

    # 修改nginx配置文件 success tomcattags
    def changeNginxConf(self, tags):
        path = Path.getInstance().runtimeDirPath + str(self.projectName) + '-node-health-status.json'
        nodehealthstatus = JsonFileFunc.getInstance().readFile(path)

        upstreamName = nodehealthstatus['upstreamName']
        nginxConfPath = nodehealthstatus['nginxConfPath']
        nginxReloadCmd = nodehealthstatus['nginxReloadCmd']
        nginxReplaceStartTag = nodehealthstatus['nginxReplaceStartTag']
        nginxReplaceEndTag = nodehealthstatus['nginxReplaceEndTag']
        nginxRootStartTag = nodehealthstatus['nginxRootStartTag']
        nginxRootEndTag = nodehealthstatus['nginxRootEndTag']
        nginxRootConf = nodehealthstatus['nginxRootConf']

        upstreamList = []
        for tag in tags:
            upstreamList.append(nodehealthstatus['nodeinfo'][tag]['upstream-str'])

        '''
        1、读取配置，读取开始标识和结束标识
        2、生成修改部分内容
        3、循环读取配置文件，找到开始标识和结束标识
        4、替换开始标识和结束标识之间的内容
        '''
        upstream_conf = nginxReplaceStartTag + '\n'
        upstream_conf += '\tupstream ' + upstreamName + '\n\t{\n'
        for upstreamStr in upstreamList:
            upstream_conf += '\t\t' + upstreamStr + '\n'
        upstream_conf += '\t\tjvm_route $cookie_JSESSIONID reverse;\n'
        upstream_conf += '\t}\n'
        upstream_conf = upstream_conf.decode('utf-8')
        root_conf = nginxRootStartTag + '\n'
        root_conf += nginxRootConf + '\n'
        root_conf = root_conf.decode('utf-8')
        FormatPrint.printInfo("modify NG upstream conf file:\n" + upstream_conf.encode('utf-8'))
        FormatPrint.printInfo("modify NG root conf file:\n" + root_conf.encode('utf-8'))
        confstr = ""

        try:
            with open(nginxConfPath, 'r') as nginx_conf_temp_file:
                isContinue = False
                isRooTContinue = False
                for line in nginx_conf_temp_file:
                    line = line.decode('utf-8')
                    # 找到这个标识,修改upstream内容
                    if line.find(nginxReplaceEndTag) != -1:
                        isContinue = False
                        confstr += upstream_conf
                    if isContinue or line.find(nginxReplaceStartTag) != -1:
                        isContinue = True
                        continue
                    # 找到这个标识,修改root内容
                    if line.find(nginxRootEndTag) != -1:
                        isRooTContinue = False
                        confstr += root_conf
                    if isRooTContinue or line.find(nginxRootStartTag) != -1:
                        isRooTContinue = True
                        continue
                    confstr += line
        except Exception as e:
            FormatPrint.printError("read nginx conf file error , the message is:\n" + str(e))
            return False
        try:
            with open(nginxConfPath, 'w') as nginx_conf_file:
                nginx_conf_file.write(confstr.encode('utf-8'))
        except Exception as e:
            FormatPrint.printError("modify nginx conf file error , the message is:\n" + str(e))
            return False
        if self.reloadNginx(nginxReloadCmd):
            return True
        else:
            return False

    # 获取upstream运行状态信息
    def getUpstreamRunstatus(self):
        nodeHealthStatusPath = Path.getInstance().runtimeDirPath + str(self.projectName) + '-node-health-status.json'
        nodeHealthStatus = JsonFileFunc.getInstance().readFile(nodeHealthStatusPath)

        upstreamStatusPath = Path.getInstance().runtimeDirPath + str(self.projectName) + '-upstream-status.json'
        upstreamStatus = JsonFileFunc.getInstance().readFile(upstreamStatusPath)
        if upstreamStatus != None:
            return upstreamStatus
        else:
            FormatPrint.printWarn(str(self.projectName) + "-upstream-status.json runtime file not exist ,will create it ")
            upstreamStatus = {
                'total-node-count': len(nodeHealthStatus["nodeinfo"].keys()),
                'upstream-node-count': len(nodeHealthStatus["nodeinfo"].keys())
            }
            for nodeName in nodeHealthStatus["nodeinfo"].keys():
                upstreamStatus[nodeName] = {
                    'last-status': 'running',
                    'is-in-upstream': True,
                    'is-rebooting': False,
                    'rebooting-count': 0,
                    'last-check-time': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            JsonFileFunc.getInstance().createFile(upstreamStatusPath, upstreamStatus)
            return upstreamStatus


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get NginxFunc Object , not given projectName")
    return NginxFunc(projectName)


# 关闭nginx
def killNginx(cmd):
    FormatPrint.printInfo("关闭nginx")
    FormatPrint.printInfo("执行命令:" + str(cmd))
    if os.system(cmd) == 0:
        FormatPrint.printInfo("关闭nginx成功")
        return True
    else:
        FormatPrint.printInfo("关闭nginx失败")
        return False


# 启动nginx
def startNginx(cmd):
    FormatPrint.printInfo("启动nginx")
    FormatPrint.printInfo("执行命令:" + str(cmd))
    if os.system(cmd) == 0:
        FormatPrint.printInfo("启动nginx成功")
        return True
    else:
        FormatPrint.printInfo("启动nginx失败")
        return False


# 删除upstream 文件
def delUpstreamStatusFile(projectName):
    orgin_file = sys.path[0] + os.sep + 'runtime' + os.sep + str(projectName) + '-upstream-status.json'
    if os.path.exists(orgin_file):
        try:
            new_file = sys.path[0] + os.sep + 'runtime' + os.sep + time.strftime('%Y%m%d%H%M%S') + str(
                projectName) + '-upstream-status.json'
            os.rename(orgin_file, new_file)
        except Exception as e:
            FormatPrint.printError("删除upstream-status文件出错:" + str(e))
            return False
        return True
    else:
        FormatPrint.printInfo("upstream-status文件不存在，未初始化")
        return True
