#!/usr/bin/env python
# !-*- coding:utf-8 -*-


import os
import until
from until import Path
from until import JsonFileFunc
from until import FormatPrint


class ConfFunc(object):
    def __init__(self, projectName=None):

        path = Path.getInstance().confDirPath + 'conf.json'
        self.projectName = projectName
        self.configure = JsonFileFunc.getInstance().readFile(path)

        self.defaultHostName = until.defaultHostName
        self.defaultUpstreamIP = until.defaultUpstreamIP
        self.defaultRebootMaxCheckCount = until.defaultRebootMaxCheckCount
        self.defaultUpdateConsumeMaxTime = until.defaultUpdateConsumeMaxTime
        self.defaultTomcatRestartMaxTime = until.defaultTomcatRestartMaxTime
        self.defaultCheckRate = until.defaultCheckRate

        # "hostName": "BBT",
        # "serverIP": "220.231.252.72",
        # "upstreamIP": "127.0.0.1",
        # "updateConsumeMaxTime": "1200",
        # "tomcatRestartMaxTime": "600",
        # "checkRate": "60",
        # "serviceCheckUrl": "/restservices/servicecheck/oamp_checkTomcatAvailable/query",
        # "serviceCheckPar": "{\"service\":\"timeservice\",\"version\":\"1.0.0\"}",
        self.hostName = self.configure['hostName'] if "hostName" in self.configure.keys() else self.defaultHostName
        self.serverIP = self.configure['serverIP']
        self.hostStr = "host:[" + self.hostName + "],IP:[" + self.serverIP + "],project:[" + self.projectName + "]"
        self.upstreamIP = self.configure['upstreamIP'] if "upstreamIP" in self.configure.keys() else self.defaultUpstreamIP
        self.updateConsumeMaxTime = self.configure['updateConsumeMaxTime'] if "updateConsumeMaxTime" in self.configure.keys() else self.defaultUpdateConsumeMaxTime
        self.tomcatRestartMaxTime = self.configure['tomcatRestartMaxTime'] if "tomcatRestartMaxTime" in self.configure.keys() else self.defaultTomcatRestartMaxTime
        self.checkRate = self.configure['checkRate'] if "checkRate" in self.configure.keys() else self.defaultCheckRate

        if projectName is None:
            FormatPrint.printError("host:" + self.hostName + ",init conf object ,not given the project name")
            FormatPrint.printFalat("host:" + self.hostName + ",init conf object ,not given the project name")

        # projectInfo 项目信息
        # "projectInfo": {
        #     "YXYBB": {
        #         "rebootMaxCheckCount": "10",
        #         "deploymentMode": "single",
        #         "tomcatScript": "tomcatstartscriptpath",
        #         "upstreamName": "YXYBB",
        #         "nginxConfPath": "C:/Users/Administrator/PycharmProjects/project-auto-update/func\\files\\nginx.conf",
        #         "nginxReloadCmd": "/usr/local/nginx/sbin/nginx -s reload",
        #         "nginxReplaceStartTag": "###NGINXREPLACE###START###YXYBB###",
        #         "nginxReplaceEndTag": "###NGINXREPLACE###END###YXYBB###",
        #         "nginxRootStartTag": "###NGINXREPLACE###ROOTSTART###YXYBB###",
        #         "nginxRootEndTag": "###NGINXREPLACE###ROOTSTART###YXYBB###",
        #         "masterGroup": {},
        #         "backupGroup":{}
        #         }
        #     }
        # }

        self.projectInfo = self.configure['projectInfo'][projectName] if projectName in self.configure['projectInfo'].keys() else None
        if self.projectInfo is None:
            FormatPrint.printError("host:" + self.hostName + ",init conf object , projectName " + projectName + " not exist the conf.json file")
            FormatPrint.printFalat("host:" + self.hostName + ",init conf object , projectName " + projectName + " not exist the conf.json file")
        self.serviceCheckUrl = self.projectInfo['serviceCheckUrl']
        self.serviceCheckPar = self.projectInfo['serviceCheckPar']
        self.rebootMaxCheckCount = self.projectInfo['rebootMaxCheckCount'] if "rebootMaxCheckCount" in self.projectInfo.keys() else self.defaultRebootMaxCheckCount
        self.deploymentMode = self.projectInfo['deploymentMode']
        self.tomcatScript = self.projectInfo['tomcatScript']
        self.startNginx = self.projectInfo['startNginx']
        self.upstreamName = self.projectInfo['upstreamName']
        self.nginxConfPath = self.projectInfo['nginxConfPath']
        self.nginxReloadCmd = self.projectInfo['nginxReloadCmd']
        self.nginxReplaceStartTag = self.projectInfo['nginxReplaceStartTag']
        self.nginxReplaceEndTag = self.projectInfo['nginxReplaceEndTag']
        self.nginxRootStartTag = self.projectInfo['nginxRootStartTag']
        self.nginxRootEndTag = self.projectInfo['nginxRootEndTag']

        # "masterGroup": {
        #                    "projectPath": "/usr/longrise/LEAP/YXYBB",
        #                    "nginxRootConf": "xxxxxxxxxxxxxxxxxxx",
        #                    "tomcats": [
        #                        {
        #                            "tag": "1",
        #                            "port": "64001"
        #                        },
        #                        {
        #                            "tag": "2",
        #                            "port": "64002"
        #                        }
        #                    ]
        #                },
        self.masterGroupInfo = self.projectInfo['masterGroup'] if "masterGroup" in self.projectInfo.keys() else None
        if self.masterGroupInfo is None:
            FormatPrint.printError("host:" + self.hostName + ",init conf object , masterGroupInfo not exist the conf.json file")
            FormatPrint.printFalat("host:" + self.hostName + ",init conf object , masterGroupInfo not exist the conf.json file")
        if self.masterGroupInfo is not None:
            self.masterProjectPath = self.masterGroupInfo['projectPath']
            self.masterNginxRootConf = self.masterGroupInfo['nginxRootConf']
            self.masterTomcatsInfo = self.masterGroupInfo['tomcats']
        self.backupGroup = self.projectInfo['backupGroup'] if "backupGroup" in self.projectInfo.keys() else None
        if self.backupGroup is None:
            FormatPrint.printError("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
            FormatPrint.printFalat("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
        if self.backupGroup is not None:
            self.backupProjectPath = self.backupGroup['projectPath']
            self.backupNginxRootConf = self.backupGroup['nginxRootConf']
            self.backupTomcatsInfo = self.backupGroup['tomcats']

    def getNginxRootConf(self, group):
        if "masterGroup" == group:
            return self.masterNginxRootConf
        if "backupGroup" == group:
            return self.backupNginxRootConf
        FormatPrint.printError("getNginxRootConf error,not get the right group")
        return "error"

    # 获取项目配置中的tomcat标识
    def getTomcatTagsByGroup(self, group):
        tags = []
        if self.projectInfo[group] is None:
            FormatPrint.printError("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
            FormatPrint.printFalat("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
        for tomcatInfo in self.projectInfo[group]['tomcats']:
            tags.append(tomcatInfo['tag'])
        return tags

    def getTomcatsByGroup(self, group):
        if self.projectInfo[group] is None:
            FormatPrint.printError("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
            FormatPrint.printFalat("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
        return self.projectInfo[group]['tomcats']

    def getTomcatsByGroups(self, groups):
        tomcats = []
        for group in groups:
            if self.projectInfo[group] is None:
                FormatPrint.printError("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
                FormatPrint.printFalat("host:" + self.hostName + ",init conf object , backupGroup not exist the conf.json file")
            tomcats = tomcats + self.projectInfo[group]['tomcats']
        return tomcats


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get ConfFunc Object , not given projectName")
    return ConfFunc(projectName)

#######################################################################################################

# print ConfFunc("YXYBB").getTomcatTagsByGroup("backupGroup")
