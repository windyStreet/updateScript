#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from until import FormatPrint
import until
import getopt
import sys
import HealthCheck
import ProjectFunc
import MailFunc
import RunningFunc
import NodeRunStatusFunc


class Controler(object):
    def __init__(self):
        pass


method = None
projectName = None
projectVersion = None
tomcatTag = None
path = None
command = None
time = None


# 平台项目更新
# -m platformupdate  -P insy
def platformupdate():
    FormatPrint.printInfo("platform will update [" + str(projectName) + "] project")
    HealthCheck.getInstance(projectName).stopHealthCheck()  # 关闭服务检查
    ProjectFunc.getInstance(projectName).replaceProjectResource()  # 替换资源
    ProjectFunc.getInstance(projectName).updateProject()  # 更新项目
    HealthCheck.getInstance(projectName).startHealthCheck()  # 启动服务检查
    version = RunningFunc.getInstance(projectName).getUpdateVersion()  # 获取更新版本
    subject = str(projectName) + "-" + str(version) + "版本更新"
    messages = RunningFunc.getInstance(projectName).getUpdateMsg()  # 获取更新信息
    level = until.mailLevel_develop  # 设置邮件发送者
    MailFunc.getInstance(projectName).sendMails(subject, messages, level)  # 发送邮件
    FormatPrint.printInfo("platform update [" + str(projectName) + "] project success")


# 平台重启项目
# -m platformRestartProject -P insy
def platformRestartProject():
    FormatPrint.printInfo("platform will restart [" + str(projectName) + "] project")
    HealthCheck.getInstance(projectName).stopHealthCheck()  # 关闭服务检查
    ProjectFunc.getInstance(projectName).restartProject()  # 重启项目
    HealthCheck.getInstance(projectName).startHealthCheck()  # 启动服务检查
    subject = str(projectName) + "-项目重启"
    messages = RunningFunc.getInstance(projectName).getUpdateMsg()  # 获取更新信息
    level = until.mailLevel_develop  # 设置邮件发送者
    MailFunc.getInstance(projectName).sendMails(subject, messages, level)  # 发送邮件
    FormatPrint.printInfo("platform restart [" + str(projectName) + "] project success")


# 平台资源替换
def platformReplaceResource():
    FormatPrint.printInfo("platform will replace " + str(projectName) + " project resources")
    updateTime = RunningFunc.getInstance(projectName).getUpdateTime()
    updateVersion = RunningFunc.getInstance(projectName).getUpdateVersion()
    ProjectFunc.getInstance(projectName).replaceProjectResource(updateVersion, updateTime)  # 替换资源

    subject = str(projectName) + "-" + str(updateVersion) + "资源替换"
    messages = RunningFunc.getInstance(projectName).getUpdateMsg()  # 获取更新信息
    level = until.mailLevel_develop  # 设置邮件发送者
    MailFunc.getInstance(projectName).sendMails(subject, messages, level)  # 发送邮件

    FormatPrint.printInfo("platform replace " + str(projectName) + " project resources success")


# 资源替换
def replaceResource():
    FormatPrint.printInfo("更新替换资源" + str(projectName) + "替换版本" + str(projectVersion))
    ProjectFunc.getInstance(projectName).replaceProjectResource(updateVersion=projectVersion, updateTime=time)  # 替换资源


# 项目更新
def update():
    FormatPrint.printInfo("script will update [" + str(projectName) + "] project")
    HealthCheck.getInstance(projectName).stopHealthCheck()  # 关闭服务检查
    ProjectFunc.getInstance(projectName).replaceProjectResource(projectVersion, time)  # 替换资源
    ProjectFunc.getInstance(projectName).updateProject()  # 更新项目
    HealthCheck.getInstance(projectName).startHealthCheck()  # 启动服务检查
    FormatPrint.printInfo("script update [" + str(projectName) + "] project success")


# 项目回滚
def rollback():
    FormatPrint.printInfo("script will rollback " + str(projectName) + "at version " + str(projectVersion))
    HealthCheck.getInstance(projectName).stopHealthCheck()  # 关闭服务检查
    ProjectFunc.getInstance(projectName).replaceProjectResource(projectVersion, time)  # 替换资源
    ProjectFunc.getInstance(projectName).updateProject()  # 更新项目
    HealthCheck.getInstance(projectName).startHealthCheck()  # 启动服务检查
    FormatPrint.printInfo("script rollback " + str(projectName) + "at version " + str(projectVersion) + " success")


# 重启项目
def restartProject():
    FormatPrint.printInfo("script will restart [" + str(projectName) + "] project")
    HealthCheck.getInstance(projectName).stopHealthCheck()  # 关闭服务检查
    ProjectFunc.getInstance(projectName).restartProject()  # 重启项目
    HealthCheck.getInstance(projectName).startHealthCheck()  # 启动服务检查
    FormatPrint.printInfo("script restart [" + str(projectName) + "] project success")


# 关闭项目
def stopProject():
    FormatPrint.printInfo("script will stop [" + str(projectName) + "] project")
    HealthCheck.getInstance(projectName).stopHealthCheck()  # 关闭服务检查
    ProjectFunc.getInstance(projectName).stopProject()  # 停止项目
    FormatPrint.printInfo("script stop [" + str(projectName) + "] project success")


# 启动项目
def startProject():
    FormatPrint.printInfo("script will start [" + str(projectName) + "] project")
    ProjectFunc.getInstance(projectName).startProject()  # 停止项目
    HealthCheck.getInstance(projectName).startHealthCheck()  # 启动服务检查
    FormatPrint.printInfo("script start [" + str(projectName) + "] project success")




# 启动健康检查服务
def startHealthCheck():
    FormatPrint.printInfo("script will start [" + str(projectName) + "] healthCheck")
    if HealthCheck.getInstance(projectName).startHealthCheck():
        FormatPrint.printInfo("script start [" + str(projectName) + "] success")
    else:
        FormatPrint.printInfo("script start [" + str(projectName) + "] failed")


# 关闭健康检查服务
def stopHealthCheck():
    FormatPrint.printInfo("script will stop [" + str(projectName) + "] healthCheck")
    if HealthCheck.getInstance(projectName).stopHealthCheck():
        FormatPrint.printInfo("script stop [" + str(projectName) + "] healthCheck success")
    else:
        FormatPrint.printInfo("script stop [" + str(projectName) + "] healthCheck failed")


# 重启健康检查服务
def restartHealthCheck():
    FormatPrint.printInfo("script will restart [" + str(projectName) + "] healthCheck")
    if HealthCheck.getInstance(projectName).restartHealthCheck():
        FormatPrint.printInfo("script restart [" + str(projectName) + "] healthCheck success")
    else:
        FormatPrint.printInfo("script restart [" + str(projectName) + "] healthCheck failed")


# 一次性健康检查服务
def healthCheckOnce():
    FormatPrint.printInfo("script will check [" + str(projectName) + "] health once")
    if HealthCheck.getInstance(projectName).checkServiceOnce():
        FormatPrint.printInfo("script check [" + str(projectName) + "] health once success")
    else:
        FormatPrint.printInfo("script check [" + str(projectName) + "] health once failed")


# 多次性健康检查服务
def healthCheckAll():
    FormatPrint.printInfo("script will check [" + str(projectName) + "] health all time")
    if HealthCheck.getInstance(projectName).checkServiceAllTime():
        FormatPrint.printInfo("script check [" + str(projectName) + "] health all time success")
    else:
        FormatPrint.printInfo("script check [" + str(projectName) + "] health all time failed")


# 查看健康检查运行状态
def healthCheckStatus():
    FormatPrint.printInfo("script get check [" + str(projectName) + "] healthCheck status")
    FormatPrint.printInfo("HealthCheck state is :" + str(HealthCheck.getInstance(projectName).getHealthCheckStatus()))


# 初始化，node-health文件
def initNodeHealthStatus():
    FormatPrint.printInfo("script will init [" + str(projectName) + "] node health file")
    if NodeRunStatusFunc.getInstance(projectName).initNodeHealthStatus():
        FormatPrint.printInfo("script init [" + str(projectName) + "] node health file success")
    else:
        FormatPrint.printInfo("script init [" + str(projectName) + "] node health file failed")


# 帮助
def help():
    print ("-h,--help")
    print (
        "-m:,--method=,will be run method:\n\
        platformReplaceResource|platformupdate|platformRestartProject|\n\
        update|stopProject|startProject|restartProject|initNodeHealthStatus|\n\
        stopHealthCheck|startHealthCheck|restartHealthCheck|healthCheckStatus|healthCheckOnce|healthCheckAll")
    print ("-u:,--update=,specify update project name")
    print ("-v:,--version=,specify projectupdate version number")
    print ("-p:,--path=,specify a detail path")
    print ("-c:,--command=,shell command")
    print ("-P:,--Project=,project name")
    print ("-t:,--Time=,project update time")

operator = \
    {
        'platformReplaceResource': platformReplaceResource,
        'platformupdate': platformupdate,
        'platformRestartProject': platformRestartProject,
        'update': update,
        'help': help,
        'startHealthCheck': startHealthCheck,
        'stopHealthCheck': stopHealthCheck,
        'restartHealthCheck': restartHealthCheck,
        'healthCheckOnce': healthCheckOnce,
        'healthCheckAll': healthCheckAll,
        'healthCheckStatus': healthCheckStatus,
        'replaceResource': replaceResource,
        'restartProject': restartProject,
        'stopProject': stopProject,
        'startProject': startProject,
        'initNodeHealthStatus': initNodeHealthStatus

    }


options, args = getopt.getopt(sys.argv[1:], "hv:p:c:m:P:t:",
                              ["help", "version=", "path=", "command=", "method=", "Project=", "Time="])

# method = "help"
if len(options) <= 0:
    if method is not None:
        FormatPrint.printFalat("已经指定方法，请使用正确方法")
    else:
        method = "help"
else:
    for name, value in options:
        if name in ['-h', '--help']:
            if method is not None:
                FormatPrint.printFalat("已经指定方法，请使用正确方法")
            else:
                method = "help"
        elif name in ['-v', '--version']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-v:--version需要参数projectVersion")
                sys.exit(1)
            projectVersion = value
        elif name in ['-p', '--path']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-p:--path需要参数filepath")
                sys.exit(1)
            path = value
        elif name in ['-c', '--command']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-c:--command需要参数command")
                sys.exit(1)
            command = value
        elif name in ['-m', '--method']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-m:--method需要参数method")
                sys.exit(1)
            method = value
        elif name in ['-P', '--Project']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-P:--Project需要参数projectname")
                sys.exit(1)
            projectName = value
        elif name in ['-t', '--Time']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-t:--Time需要参数timestamp")
                sys.exit(1)
            time = value
        else:
            method = "help"
operator.get(method)()
