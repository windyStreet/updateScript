#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from until import FormatPrint
import time
import NginxFunc
from until import JsonFileFunc
from until import Path
import TomcatFunc
import ConfFunc


class NginxUpstreamCheck(object):
    def __init__(self, projectName):
        self.projectName = projectName
        self.nodeHealthStatus = JsonFileFunc.getInstance().readFile(Path.getInstance().runtimeDirPath + str(self.projectName) + '-node-health-status.json')
        self.upstreamStatus = NginxFunc.getInstance(self.projectName).getUpstreamRunstatus()

    # 检查upstream
    def checkUpstream(self):
        alive_count = 0
        alive_nodes = []
        dead_count = 0
        dead_nodes = []
        upstream_changed = False

        node_health_status = self.nodeHealthStatus['nodeinfo']
        upstream_status = self.upstreamStatus

        tomcatScript = self.nodeHealthStatus['tomcatScript']

        for node_name in sorted(node_health_status.keys()):
            if node_health_status[node_name]['status'] == 'running' or \
                            node_health_status[node_name]['status'] == 'error' or \
                            node_health_status[node_name]['status'] == 'n/a':
                alive_count += 1
                alive_nodes.append(node_name)

            if node_health_status[node_name]['status'] == 'dead':
                dead_nodes.append(node_name)
                dead_count += 1

            if (upstream_status[node_name]['last-status'] == 'running' or
                        upstream_status[node_name]['last-status'] == 'error' or
                        upstream_status[node_name]['last-status'] == 'n/a') and \
                            node_health_status[node_name]['status'] == 'dead':
                upstream_changed = True

            if upstream_status[node_name]['last-status'] == 'dead' and node_health_status[node_name]['status'] == 'running':
                upstream_changed = True

        if alive_count == 0:
            FormatPrint.printError(" no lived node, abort upstream edit ")
        elif upstream_changed:
            FormatPrint.printInfo(" upstream changed , nginx need to modify ")
            NginxFunc.getInstance(self.projectName).changeNginxConf(alive_nodes)

        latest_upstream_status = {
            'total-node-count': alive_count + dead_count,
            'upstream-node-count': alive_count
        }

        for alive_node_key in alive_nodes:
            latest_upstream_status[alive_node_key] = {
                'last-status': node_health_status[alive_node_key]['status'],
                'is-in-upstream': True,
                'is-rebooting': False,
                'rebooting-count': 0,
                'last-check-time': time.strftime('%Y-%m-%d %H:%M:%S')
            }

        for dead_node_key in dead_nodes:
            is_rebooting = True
            rebooting_count = upstream_status[dead_node_key]['rebooting-count']
            if upstream_status[dead_node_key]['is-rebooting'] is False:
                FormatPrint.printInfo('restart dead node ' + dead_node_key)
                TomcatFunc.getInstance().restartTomcat(tomcatScript, dead_node_key)
                FormatPrint.printInfo("restart tomcat" + str(dead_node_key) + " finished")
            else:
                rebooting_count += 1
                FormatPrint.printInfo('dead node ' + str(dead_node_key) + ' is in rebooting count: ' + str(rebooting_count))
                if rebooting_count % int(ConfFunc.getInstance(self.projectName).rebootMaxCheckCount) == 0:
                    is_rebooting = False

            latest_upstream_status[dead_node_key] = {
                'last-status': node_health_status[dead_node_key]['status'],
                'is-in-upstream': False,
                'is-rebooting': is_rebooting,
                'rebooting-count': rebooting_count,
                'last-check-time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        upstreamPath = Path.getInstance().runtimeDirPath + str(self.projectName) + '-upstream-status.json'
        JsonFileFunc.getInstance().createFile(upstreamPath, latest_upstream_status)


def getInstance(projectName):
    if projectName is None:
        FormatPrint.printFalat("get NginxUpstreamCheck Object , not given projectName")
    return NginxUpstreamCheck(projectName)
