#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import time
import sys
import os
import Path


class FormatPrint(object):
    def __init__(self):
        pass


# 格式化info输出
def printInfo(object):
    log = "[ INFO]" + time.strftime('%Y-%m-%d %H:%M:%S') + "  " + str(object)
    writeLogFile(log, "info")
    print(log)


# 格式化error输出
def printError(object):
    log = "[ERROR]" + time.strftime('%Y-%m-%d %H:%M:%S') + "  " + str(object)
    writeLogFile(log, "err")
    print(log)


# 格式化warn输出
def printWarn(object):
    log = "[ WARN]" + time.strftime('%Y-%m-%d %H:%M:%S') + "  " + str(object)
    writeLogFile(log, "war")
    print(log)


# 格式化debug输出
def printDebug(object):
    log = "[DEBUG]" + time.strftime('%Y-%m-%d %H:%M:%S') + "  " + str(object)
    writeLogFile(log, "debug")
    print(log)


# 格式化fatal输出
def printFalat(object):
    log = "[FALAT]" + time.strftime('%Y-%m-%d %H:%M:%S') + "  " + str(object)
    writeLogFile(log, "falat")
    print(log)
    sys.exit(1)


# 日志文件写入
def writeLogFile(logStr, type):
    logPath = Path.getInstance().logsDirPath + 'log.log'
    if type == 'info':
        systematicPath = Path.getInstance().logsDirPath + 'info.log'
    elif type == 'err':
        systematicPath = Path.getInstance().logsDirPath + 'error.log'
    elif type == 'war':
        systematicPath = Path.getInstance().logsDirPath + 'warning.log'
    elif type == 'debug':
        systematicPath = Path.getInstance().logsDirPath + 'debug.log'
    elif type == 'falat':
        systematicPath = Path.getInstance().logsDirPath + 'falat.log'
    else:
        systematicPath = Path.getInstance().logsDirPath + 'log.log'

    with open(systematicPath, 'a+') as type_log_file:
        type_log_file.write(logStr + '\n')

    with open(logPath, 'a+') as log_file:
        log_file.write(logStr + '\n')

    systematicSize = os.path.getsize(systematicPath)
    if (systematicSize / 1024 / 1024) > 30:
        systematic_file = Path.getInstance().logsDirPath + time.strftime('%Y-%m-%d-%H-%M-%S') + "-" + systematicPath.split(os.sep)[-1]
        os.rename(systematicPath, systematic_file)

    logSize = os.path.getsize(logPath)
    if (logSize / 1024 / 1024) > 30:
        log_file = Path.getInstance().logsDirPath + time.strftime('%Y-%m-%d-%H-%M-%S') + "-" + logPath.split(os.sep)[-1]
        os.rename(logPath, log_file)
