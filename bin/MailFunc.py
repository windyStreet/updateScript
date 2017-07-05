#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from until import JsonFileFunc
from until import Path
from until import FormatPrint


class MailFunc(object):
    def __init__(self, projectName):
        self.projectName = projectName
        self.mailConf = None
        self.message = None
        self.subject = None
        self.sendLevel = None  # 发送等级
        self.senderMailAccount = None  # 发送者邮箱账户
        self.senderMailName = None  # 发送者名称
        self.senderMailPassword = None  # 发送者邮箱账户密码
        self.SMTPName = None  # SMTP 名称
        self.SMTPPort = None  # SMTP 端口

        path = Path.getInstance().confDirPath + str(self.projectName) + '-mail-conf.json'
        mailConfInfo = JsonFileFunc.getInstance().readFile(path)
        if mailConfInfo is None:
            FormatPrint.printError(str(self.projectName) + "mail-conf.json file is not exist")
            FormatPrint.printFalat(str(self.projectName) + "mail-conf.json file is not exist,exit!")
        else:
            self.mailConf = mailConfInfo  # 配置信息
            self.senderMailAccount = mailConfInfo['SMTP']['senderMailAccount']  # 发送者邮箱账户
            self.senderMailName = mailConfInfo['SMTP']['senderMailName']  # 发送者名称
            self.senderMailPassword = mailConfInfo['SMTP']['senderMailPassword']  # 发送者邮箱账户密码
            self.SMTPName = mailConfInfo['SMTP']['name']  # SMTP 名称
            self.SMTPPort = mailConfInfo['SMTP']['port']  # SMTP 端口

    # 发送邮件
    def sendMail(self):
        msg = MIMEText(self.message, 'plain', 'utf-8')
        receiverAccounts = []
        receiverNames = []
        for receiverInfo in self.mailConf['receiver']:
            if str(receiverInfo['level']) <= str(self.sendLevel):
                receiverAccounts.append(receiverInfo['email'])
                receiverNames.append(receiverInfo['name'])

        receiverAccounts = list(set(receiverAccounts))
        receiverNames = list(set(receiverNames))

        receiverNamesStr = str((",".join(receiverNames)).encode('utf-8'))
        receiverNamesStr = "[" + receiverNamesStr + "]"

        msg['From'] = formataddr([self.senderMailName, self.senderMailAccount])  # 显示发件人信息
        msg['To'] = ";".join(receiverAccounts)  # 显示收件人信息
        msg['Subject'] = self.subject  # 定义邮件主题
        server = None
        try:
            # 创建SMTP对象
            server = smtplib.SMTP(self.SMTPName, int(self.SMTPPort))
            # server.set_debuglevel(1)  # 可以打印出和SMTP服务器交互的所有信息
            # login()方法用来登录SMTP服务器
            server.login(self.senderMailAccount, self.senderMailPassword)
            # sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文是一个str，as_string()把MIMEText对象变成str

            if len(receiverAccounts) <= 0:
                FormatPrint.printInfo("can not get the sender info ")
            else:
                server.sendmail(self.senderMailAccount, receiverAccounts, msg.as_string())
                FormatPrint.printInfo("the mail <" + str(self.subject) + "> send to " + str(receiverNamesStr) + "mail box")
        except Exception as e:
            FormatPrint.printError("can not send mail , exception is :" + str(e))
        finally:
            if server is None:
                FormatPrint.printInfo("can not init mail server")
            else:
                server.quit()

    # 发送邮件定义
    def sendMails(self, subject, messages, level):
        self.subject = subject
        self.message = messages
        self.sendLevel = level
        self.sendMail()


def getInstance(projectName=None):
    if projectName is None:
        FormatPrint.printFalat("get MailFunc Object , not given projectName")
    return MailFunc(projectName)
