#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import socket

defaultCheckRate = 60  # 默认检查频率60s
defaultHostName = socket.gethostname()  # 默认主机名
defaultRebootMaxCheckCount = 5  # 默认重启最大检查次数 5次，即tomcat关闭后，5次检查内无法启动则重新骑宠
defaultUpdateConsumeMaxTime = 300  # 默认更新花费最大时间300s
defaultTomcatRestartMaxTime = 300  # 默认tomcat重启最大时间（在更新过程中）
defaultUpstreamIP = "127.0.0.1"  # 默认upstream的ip配置
env = "online"
mailLevel_admin = 10
mailLevel_tester = 20
mailLevel_product = 30
mailLevel_develop = 40
mailLevel_default = 30
