#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# @script name   send FRMON cmd to telnet port
# @version               v1
# @date                  2014-10-15
# @author                Yunpeng
# @draft                 Yunpeng
#
# @Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import sys
import telnetlib
import argparse
import time

configFilePath = "config.ini"
para = ["frmonIP_1","frmonIP_2","port","timeout","send_gap","frmonCmdLines"]

def readconfig():
    paraD = {}
    #    Load file with config parameters
    file1 = open(configFilePath, 'r')
    try:
        lines1 = file1.readlines()
    finally:
        file1.close()

    for line in lines1:
        for i in range(len(para)):
            if line.find(para[i]) != -1:
                tmp_args = line.split("=")
                value = tmp_args[1].strip("\n")
                print ('Get parameter : %s = %s' % (para[i],value))
                paraD.setdefault(para[i],value)
    #print paraD
    return paraD

readconfig()