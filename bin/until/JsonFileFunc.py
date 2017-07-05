#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import FormatPrint
import json
import codecs


class JsonFileFunc(object):
    def __init__(self):
        pass

    # read content
    def readFile(self, fielPath):
        jsonData = None
        try:
            with open(fielPath, 'r') as tmpFile:
                jsonData = json.load(tmpFile)
        except Exception as e:
            FormatPrint.printError("read [ " + str(fielPath) + " ] not exists")
            FormatPrint.printError("errorMsg:" + str(e))
        return jsonData

    # create json File
    def createFile(self, fielPath, data):
        try:
            with codecs.open(fielPath, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(json.dumps(data, ensure_ascii=False, indent=4))
        except Exception as e:
            FormatPrint.printFalat('create ' + str(fielPath) + ' fail')
            FormatPrint.printError("errorMsg:" + str(e))


def getInstance():
    return JsonFileFunc()
