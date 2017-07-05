#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import sys
import os

__author__ = 'windyStreet'
__time__ = '2017-03-17'


class Path(object):
    def __init__(self):
        self.path = sys.path[0]
        self.projectDirPath = self.path[0:self.path.rindex("bin")]
        self.confDirPath = self.projectDirPath + "conf" + os.sep
        self.logsDirPath = self.projectDirPath + "logs" + os.sep
        self.scriptsDirPath = self.projectDirPath + "scripts" + os.sep
        self.filesDirPath = self.projectDirPath + "files" + os.sep
        self.runtimeDirPath = self.projectDirPath + "runtime" + os.sep
        pass


def getInstance():
    return Path()
