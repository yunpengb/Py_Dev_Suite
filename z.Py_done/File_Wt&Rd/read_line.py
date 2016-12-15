#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# @version               v1
# @date                  2015-10-10
# @author                Yunpeng
#
# @Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import sys
import os.path
import linecache
import telnetlib

unitIP = "192.168.255.69"
FRMport = 200
tnFR = telnetlib.Telnet(unitIP, FRMport)
 

def lineContent(textfile,linenum):
    line = linecache.getline(textfile,linenum)
    return line

def checkfrmonDone(tn,cmd,ack):
    sendcmd = str(cmd)
    print "==>FRMON input: [%s]" % sendcmd
    tn.write(sendcmd+"\n")
    ra = tn.read_until("==>")
    rb = tn.read_until(">")
    ra = removeCmdEmptyStr(ra)
    rb = removeAckEmptyStr(rb)
    r = ra + rb
    print "<==FRMON output: [%s]" % r
    if rb == ack:
        return True
    else:
        return False
        
def removeCmdEmptyStr(strin):
    a1 = strin.strip()
    a2 = a1.strip()
    a3 = a2.strip("\n")
    return a3
    
def removeAckEmptyStr(strin):
    a1 = strin.strip()
    a2 = a1.strip(">")
    a3 = a2.strip()
    a4 = a3.strip("\n")
    return a4

file = "D:\\byp\\TOPIC\\DL_gain\\DL_gain_fenxi\\cmdset\\FHEI_1842.5.csv"
nu = 10
a = lineContent(file,nu)
#print a
a1 = a.split(',')
#print "@_@Cmd is:[%s]" % a1[0]
#print "@_@ExpectAck is:[%s]" % removeEmptyStr(a1[1])
cmd = a1[0]
ac1 =a1[1]
ac2 = ac1.strip()
expectAck = ac2.rstrip('>')

result = checkfrmonDone(tnFR,cmd,expectAck)
if result :
    #print result
    print "Yes,result is done!"
    print "true end"
else:
    #print result
    print 'sth is wrong!'
    sys.exit("================ ack is not expect,stop! ================")
    print "false end"
    
print "see end"



