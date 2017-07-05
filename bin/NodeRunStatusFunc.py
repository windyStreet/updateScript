#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import time
from until import FormatPrint
from until import JsonFileFunc
import ConfFunc
import RunningFunc
from until import Path


class NodeRunStatusFunc(object):
    def __init__(self, projectName):
        self.projectName = projectName
        self.conFuncObj = ConfFunc.getInstance(self.projectName)
        pass

    # 每次更新时，重新初始node 文件
    def initNodeHealthStatus(self):
        # 将要被更新的组
        willUpdateGroups = RunningFunc.getInstance(self.projectName).getWillUpdateGroups(self.conFuncObj.deploymentMode)
        newTomcats = []
        for group in willUpdateGroups:
            tomcats = self.conFuncObj.getTomcatsByGroup(group)
            for tomcat in tomcats:
                newTomcats.append(tomcat)

        serviceCheckUrl = self.conFuncObj.serviceCheckUrl
        serviceCheckPar = self.conFuncObj.serviceCheckPar

        upstreamName = self.conFuncObj.upstreamName
        nginxConfPath = self.conFuncObj.nginxConfPath
        nginxReloadCmd = self.conFuncObj.nginxReloadCmd
        nginxReplaceStartTag = self.conFuncObj.nginxReplaceStartTag
        nginxReplaceEndTag = self.conFuncObj.nginxReplaceEndTag
        nginxRootStartTag = self.conFuncObj.nginxRootStartTag
        nginxRootEndTag = self.conFuncObj.nginxRootEndTag
        nginxRootConf = self.conFuncObj.getNginxRootConf(willUpdateGroups[0])
        tomcatScript = self.conFuncObj.tomcatScript

        node_health_status = {
            "currentRunGroups": willUpdateGroups,
            "nginxConfPath": nginxConfPath,
            "upstreamName": upstreamName,
            "nginxReloadCmd": nginxReloadCmd,
            "nginxReplaceStartTag": nginxReplaceStartTag,
            "nginxReplaceEndTag": nginxReplaceEndTag,
            "nginxRootStartTag": nginxRootStartTag,
            "nginxRootEndTag": nginxRootEndTag,
            "nginxRootConf": nginxRootConf,
            "tomcatScript": tomcatScript,
            "nodeinfo": {}
        }

        for tomcat in newTomcats:
            node_name = tomcat['tag']
            health_check_url = "http://" + self.conFuncObj.serverIP + ":" + tomcat["port"] + serviceCheckUrl
            srun_id = node_name if int(node_name) > 10 else '0' + str(node_name)
            upstreamStr = "server " + self.conFuncObj.upstreamIP + ":" + str(tomcat["port"]) + " max_fails=5 fail_timeout=60s weight=1 srun_id=" + str(srun_id) + ";"
            nodeDetail = {
                'health-check-url': health_check_url,
                'health-check-data': serviceCheckPar,
                'status': 'n/a',
                'last-response-data': 'n/a',
                'last-response-time': 0,
                'fail-count': 0,
                'last-check-time': time.strftime('%Y-%m-%d %H:%M:%S'),
                "upstream-str": str(upstreamStr)
            }
            node_health_status['nodeinfo'][node_name] = nodeDetail
        path = Path.getInstance().runtimeDirPath + str(self.projectName) + '-node-health-status.json'
        JsonFileFunc.getInstance().createFile(path, node_health_status)
        return True

    # 获取节点运行状态信息
    def getNodeRunStatusInfo(self):
        path = Path.getInstance().runtimeDirPath + str(self.projectName) + '-node-health-status.json'
        return JsonFileFunc.getInstance().readFile(path)


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get NodeRunStatusFunc Object , not given projectName")
    return NodeRunStatusFunc(projectName)


'''
    "1": {
        "status": "n/a",
        "health-check-url": "http://220.231.252.72:64001/LSIP/restservices/servicecheck/oamp_checkTomcatAvailable/query",
        "last-response-data": "n/a",
        "last-response-time": 0,
        "fail-count": 0,
        "last-check-time": "2016-12-01 16:37:09",
        "health-check-data": "{\"service\":\"timeservice\",\"version\":\"1.0.0\"}"
    },
    "2": {
        "status": "n/a",
        "health-check-url": "http://220.231.252.72:64002/LSIP/restservices/servicecheck/oamp_checkTomcatAvailable/query",
        "last-response-data": "n/a",
        "last-response-time": 0,
        "fail-count": 0,
        "last-check-time": "2016-12-01 16:37:09",
        "health-check-data": "{\"service\":\"timeservice\",\"version\":\"1.0.0\"}"
    },
    "currentrun": "groupmaster",
    "deploymentmode": "single"
'''

# init node-health-status file
'''
初始化node-health-status
'''

# modify node-health-status file
'''
修改nodehealthstatus 文件内容
注：修改过程为每次重新初始化该文件（避免修改过程过程比较繁琐），且在onehalf模式中存在不同组中的数据进行组合问题
'''


def modifyNodeHealthStatus(pu):
    projecName = pu.projectName
    deploymentmode = pu.deploymentmode
    tomcatGroup = pu.willUpdateGroup

    tomcat_conf = pu.projectJson.tomcatConf
    tomcatTags = tomcat_conf['projectname'][projecName][tomcatGroup]['tomcatgroupinfo']['tomcats']
    servicecheckurl = tomcat_conf['projectname'][projecName][tomcatGroup]['servicecheckurl']
    servicecheckpar = tomcat_conf['projectname'][projecName][tomcatGroup]['servicecheckpar']
    currentRunGroup = pu.willUpdateGroup

    if deploymentmode == 'single':
        FormatPrint.printError(" you must be joking , no posslible ")
    elif deploymentmode == 'onehalf':
        FormatPrint.printInfo(" onehalf mode modify node-health-status ")
    elif deploymentmode == 'double':
        FormatPrint.printInfo(" double mode modify node-health-status ")
    else:
        FormatPrint.printFalat(" you must bu configure worng deploymentmode ")
