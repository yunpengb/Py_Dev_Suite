#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# @version               v1
# @Script name          TX gain calibration
# @date                  2015-10-10
# @author                Yunpeng
#
# @Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import sys
import os.path
import linecache
import telnetlib
import time
import re
from ftplib import FTP
import def1
from def1 import *


hostIP = "192.168.255.69"
fsvIP = "192.168.1.2"
FRMport = 200
SHport = 2323
tnFR = telnetlib.Telnet(hostIP,FRMport)
tnSH = telnetlib.Telnet(hostIP,SHport)

rootdir = getrootDir()
logdir = rootdir + "\\log"
resourceDir = rootdir + "\\resource"
dlGainSeqfile = resourceDir + "\\FRMONcmd.csv"
rcal = "rcal.xml"
calf = "calf.xml"
emptyRCALlocat = resourceDir + "\\" + rcal
emptyCAFLlocat = resourceDir + "\\" + calf
LTE5locat = resourceDir + "\\data_LTE5.bin"

shellcmd1 = "flash -d 3"
shellcmd2 = "flash -f RCAL rcal.xml 3 ON"
shellcmd3 = "flash -f CALF calf.xml 3 ON"
shellcmd4 = "flash -r RCAL ON"
shellcmd5 = "flash -r CALF ON"
shellcmd6 = "flash -u RCAL rcal.xml 3 ON"
shellcmd7 = "flash -u CALF calf.xml 3 ON"
shellcmd8 = ""

freq_tx = ["1807.5","1835","1862.5"]
freq_rx = ["1712.5","1740","1767.5"]
incableloss = ["45.9","45.9","45.9"]

tx_mark = ["","",""]
rx_mark = ["","",""]
calibResult = [[None for x in range(4)] for y in range(3)]

for i in range(3):
 tx_mark[i] = int(float(freq_tx[i])*1000)
 rx_mark[i] = int(float(freq_rx[i])*1000)


#============== create work space ==============
timestamp = maketimestamp("all")
logmark = "DLgain_log_" + timestamp
currentlogDir = logdir + "\\" +logmark
os.mkdir(currentlogDir)
logname = currentlogDir + "\\" + logmark + ".txt"
log = makeNewlog(logname)
#===============================================


#===== check calibration stat and replace empty =======
caliFileStat = sendShell(tnSH,shellcmd1,log,1)
RCALdownlocat = currentlogDir + "\\" + rcal
CALFdownlocat = currentlogDir + "\\" + calf

if "RCAL" in caliFileStat:
    print "===RCAL is exist,backup it~~"
    sendShell(tnSH,shellcmd2,log)
    wait(2)
    ftp_down(hostIP,RCALdownlocat,"rcal.xml")
    wait(1)
    print "===remove RCAL"
    sendShell(tnSH,shellcmd4,log)
if "CALF" in caliFileStat:
    print "===CALF is exist,backup it~~"
    sendShell(tnSH,shellcmd3,log)
    wait(2)
    ftp_down(hostIP,CALFdownlocat,"calf.xml")
    wait(1)
    print "===remove CALF"
    sendShell(tnSH,shellcmd5,log)

wait(1)


for i in range(3):
# make a loop for B/M/T freq tx-gain calibration 

    caliFileStat = sendShell(tnSH,shellcmd1,log)
    if "RCAL" not in caliFileStat and "CALF" not in caliFileStat:
        logit("===OK,all cali file is clear.\n",log)

    logit("===ftpUp empty cali files.\n",log)
    ftp_up(hostIP,emptyRCALlocat,rcal)
    ftp_up(hostIP,emptyCAFLlocat,calf)
    wait(1)
    logit("===UU the new cali files.\n",log)
    sendShell(tnSH,shellcmd6,log)
    sendShell(tnSH,shellcmd7,log)
    wait(1)

    caliFileStat = sendShell(tnSH,shellcmd1,log)
    if "RCAL" in caliFileStat and "CALF" in caliFileStat:
        logit("===replace empty cali file done.\n",log)
    else:
        logit("===sth is wrong,replace cali file error.\n",log)
        sys.exit("================ ERR: UU the new cali file error,stop! ================")
    #===============================================


    #================================== send FRMON cmd =====================================
    ftp_up(hostIP,LTE5locat,"data_LTE5.bin")
    wait(1)
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,5,7,log,tnFR)

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,10,11,log,tnFR)
    
    #================ setup(config) TX carrier ===============
    txCmd1 = modifylinetoStr(dlGainSeqfile,12,"TXfrequ",str(tx_mark[i]),log)
    #print txCmd1
    sendfrmon(tnFR,txCmd1,log)
    wait(1)
    #===========================
    
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,13,13,log,tnFR)
    
    #================ setup(config) RX carrier ===============
    rxCmd1 = modifylinetoStr(dlGainSeqfile,14,"RXfrequ",str(rx_mark[i]),log)
    #print rxCmd1
    sendfrmon(tnFR,rxCmd1,log)
    wait(1)
    #===========================
    
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,15,16,log,tnFR)
    wait(4)

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,19,19,log,tnFR)

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,22,24,log,tnFR)

    #=== get G1 offset ====
    ack1 = sendlineToFRmon(dlGainSeqfile,27,log,tnFR)
    #print "ack is [%s]" % ack1
    ack2 = re.search(r'-(\d+)\.(\d+)', ack1)
    offset = float(ack2.group(0))
    #===============================

    #================================== read power =========================================
    FSV = FSVtn(fsvIP)
    FSV.FSV_prepare("5",freq_tx[i],incableloss[i],log)
    outpower = FSV.FSV_readPower(3,log)
    print "power is [%s]" % outpower
    print "offset is [%s]" % offset

    #== calc the Ggain ===
    Ggain = 37 - outpower + offset
    print "gain = 37-power + offset = [%s]" % Ggain

    #================ get VVA word ===============
    newCmd1 = modifylinetoStr(dlGainSeqfile,32,"G1gain",str(Ggain),log)
    #print newCmd1
    sendfrmon(tnFR,newCmd1,log)
    wait(5)
    vva1 = sendlineToFRmon(dlGainSeqfile,35,log,tnFR)
    #print "vva1 is [%s]" % vva1
    vva2 = re.search(r'\d{4}', vva1)
    vvaWord = int(vva2.group(0))
    print "vvaWord is [%s]" % vvaWord
    #=============================================

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,36,37,log,tnFR)

    #=========== get RFchain1 temperature ========
    temp1 = sendlineToFRmon(dlGainSeqfile,38,log,tnFR)
    print "temp1 is [%s]" % temp1

    temp2 = re.search(r'(\d{2})\.(\d+)', temp1)
    rfChainTemp = float(temp2.group(0))
    print "rfChainTemp is [%s]" % rfChainTemp
    #=============================================
    
    wait(3)
    # destory the carrier(1tx+1rx)
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,41,44,log,tnFR)
    wait(5)
    logit(("[End] the TX calibration for []Mhz is done." % freq_tx),log)
    calibResult[i] = [Ggain,tx_mark[i],rfChainTemp,vvaWord]
print calibResult
    
