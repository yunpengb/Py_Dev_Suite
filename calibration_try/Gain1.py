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


hostIP = "192.168.255.69"
fsvIP = "192.168.1.2"
FRMport = 200
SHport = 2323
tnFR = telnetlib.Telnet(hostIP,FRMport)
tnSH = telnetlib.Telnet(hostIP,SHport)


def getrootDir():
    homedir = os.getcwd()
    return homedir

def ftp_up(host,locatfile,filename,port = "21"):
    ftp=FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host,port)
    ftp.login('','')
    #print ftp.getwelcome()#显示ftp服务器欢迎信息
    #ftp.cwd('xxx/xxx/') #选择操作目录
    bufsize = 1024#设置缓冲块大小
    file_handler = open(locatfile,'rb')#以读模式在本地打开文件
    ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize)#上传文件
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    print "<>ftp up OK"

def ftp_down(host,filelocation,filename,port = "21"):
    ftp=FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host,port)
    ftp.login('','')
    #print "<>" + ftp.getwelcome()#显示ftp服务器欢迎信息
    #ftp.cwd('xxx/xxx/') #选择操作目录
    bufsize = 1024
    file_handler = open(filelocation,'wb').write #以写模式在本地打开文件
    ftp.retrbinary('RETR %s' % os.path.basename(filename),file_handler,bufsize)#接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)
    #file_handler.close()
    ftp.quit()
    print "<>ftp down OK"

def logit(text,log,i = 1):
    time = maketimestamp("time")
    log.write("<log>-" + time + " " + text + "\n")
    if i == 1:
        print "<log>-" + time + " " + text + "\n"

def getlineContent(textfile,linenum):
    a = linecache.getline(textfile,linenum)
    a1 = a.split(',')
    return a1

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

def makeNewlog(name):
    log = open(name, 'w')
    return log

def maketimestamp(instr):
    if instr == "time":
        timestamp = time.strftime('%H:%M:%S',time.localtime(time.time()))
    elif instr == "all":
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
    elif instr == "date":
        timestamp = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    else:
        print "WRONG,timeStampMake-keyword is not support!"
        timestamp = "[time_WRONG]"
    return timestamp

def checkStrContain(text,word):
    if word in text:
        en = True
    else:
        en = False
    return en

def checkdirExist(dir):
    a = os.path.exists(dir)
    return a

def checkdir(dir,operat,log):
    if not checkdirExist(dir):
        os.mkdir(dir)
        logit(("<>folder not exist! create a empty dir: [%s]\n" % dir),log)
    else:
        if operat == "empty" :
            removeFileInFirstDir(dir)
            logit(("<>empty the folder: [%s]\n" % dir),log)
        elif operat == "check" :
            logit(("<>folder exist,do nothing: %s \n" % dir),log,0)
    logit(("<>check folder done,OK~: [%s]\n" % dir),log,0)

def wait(t):
    time.sleep(t)

def sendfrmon(tn,cmd,log):
    sendcmd = str(cmd)
    logit(("==>FRMON input: [%s]\n" % sendcmd),log)
    tn.write(sendcmd+"\n")
    ra = tn.read_until("==>")
    rb = tn.read_until(">")
    ra = removeCmdEmptyStr(ra)
    rb = removeAckEmptyStr(rb)
    r = ra + rb
    logit(("<==FRMON output: [%s]\n" % r),log,0)
    return rb

def sendShell(tn,cmd,log,off=0):
    sendcmd = str(cmd)
    logit(("==>SHELL input: [%s]\n" % sendcmd),log)
    tn.write(sendcmd+"\n")
    ac = tn.read_until("@")
    if off == 1:
        ac = tn.read_until("@")
    ack = removeCmdEmptyStr(ac)
    logit(("<==SHELL output: [%s]\n" % ack),log,0)
    return ack

def sendlineToFRmon(file,linenum,log):
    lineContent = getlineContent(file,linenum)
    cmd = lineContent[0]
    ack = sendfrmon(tnFR,cmd,log)
    return ack

def sendModifylineToFRmon(file,linenum,origWord,replaceWord,log):
    lineContent = getlineContent(file,linenum)
    cmd = lineContent[0]
    newCmd = cmd.replace(origWord,replaceWord)
    #ack = sendfrmon(tnFR,newCmd,log)
    #return ack
    return newCmd

def sendfewlinetoFRmonandCheckAck(file,beginlineNum,endlineNum,log):
    for i in range(beginlineNum,endlineNum+1):
        lineContent = getlineContent(file,i)
        cmd = lineContent[0]
        ea = lineContent[1]
        expectAck = ea.strip()
        realAck = sendfrmon(tnFR,cmd,log)
        '''
        if realAck == expectAck:
            logit("<>realAck is equal to expectAck!done.Next frmon cmd.\n",log)
            continue
        else:
        '''
        if 1 == 1:
            #logit("<>sth is wrong,realAck is not the expectAck.\n",log)
            logit(("<>expectAck is [%s]\n" % expectAck),log)
            logit(("<>realAck is [%s]\n" % realAck),log)
            #sys.exit("================ ERR: sth happen ,realAck is not equal to expectAck. ================")

class FSVtn(object):
    global FSVport
    
    FSVport = 5025
    
    def __init__(self,fsvip):
        global fsvtn
        try:
            fsvtn = telnetlib.Telnet(fsvip, FSVport)
            print "[FSVtn] connect to FSV done!"
        except:
            print "can't access to FSV via telnet!"

    def FSV_prepare(self,bandwidth,freq,inCableLoss,log):
        'make FSV ready in LTE mode'
        dict_SupportBands = {'1.4':'1_40', '3':'3_00', '5':'5_00','10':'10_00','15':'15_00','20':'20_00'}
        band = dict_SupportBands[bandwidth]
        fsvPre = ["*RST","INIT:CONT OFF","SYST:DISP:UPD ON","INST LTE","CONF:DL:BW BW"+band,"POW:AUTO2 ON","DISP:TRAC:Y:RLEV:OFFS "+inCableLoss,"CALC2:FEED 'SPEC:ACP'","FREQ:CENT "+freq+"MHz",]
        print "[FSVtn] FSV reseting and preparing~"
        for i in range(0,len(fsvPre)):
            fsvtn.write(fsvPre[i] + "\n")
            wait(2)
            #print("==> SEND : %s " % fsvPre[i])
            #log.write('[FsvPrepare] ==> SEND : %s \r\n' % str(fsvPre[i]) )
        logit('[FsvPrepare] FSV is prepared in LTE mode!',log)
        wait(1)

    def FSV_readPower(self,meantimes,log):
        outpower = [-100]*meantimes
        for i in range(0,meantimes):
            fsvtn.write("INIT;*WAI\n") # execute test
            logit("[FSV_readPower] execute test.(%s/%s)" % (i+1,meantimes),log)
            wait(1)
            fsvtn.write("CALC1:MARK:FUNC:POW:RES?\n") # ask for aclr result
            logit("[FSV_readPower] Reading Power form FSV.(%s/%s)" % (i+1,meantimes),log)
            wait(1)
            temp = fsvtn.read_very_eager()
            data = temp.split(',')
            logit("[FSV_readPower] get power " + data[0],log)
            outpower[i] = float(data[0])
        pwr = sum(outpower)/meantimes
        return pwr


rootdir = getrootDir()
logdir = rootdir + "\\log"
resourceDir = rootdir + "\\resource"
dlGainSeqfile = resourceDir + "\\FHEI_1842.5.csv"
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
 rx_mark[1] = int(float(freq_rx[1])*1000)


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
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,5,7,log)

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,10,11,log)
    
    #================ setup(config) TX carrier ===============
    txCmd1 = sendModifylineToFRmon(dlGainSeqfile,12,"TXfrequ",str(tx_mark[i]),log)
    #print txCmd1
    sendfrmon(tnFR,txCmd1,log)
    wait(1)
    #===========================
    
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,13,13,log)
    
    #================ setup(config) RX carrier ===============
    rxCmd1 = sendModifylineToFRmon(dlGainSeqfile,14,"RXfrequ",rx_mark[i],log)
    #print rxCmd1
    sendfrmon(tnFR,rxCmd1,log)
    wait(1)
    #===========================
    
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,15,16,log)
    wait(4)

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,19,19,log)

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,22,24,log)

    #=== get G1 offset ====
    ack1 = sendlineToFRmon(dlGainSeqfile,27,log)
    #print "ack is [%s]" % ack1
    ack2 = re.search(r'-(\d+)\.(\d+)', ack1)
    offset = float(ack2.group(0))
    #===============================

    #================================== read power =========================================
    FSV = FSVtn(fsvIP)
    FSV.FSV_prepare("5",freq_tx[i],incableloss,log)
    outpower = FSV.FSV_readPower(3,log)
    print "power is [%s]" % outpower
    print "offset is [%s]" % offset

    #== calc the Ggain ===
    Ggain = 37 - outpower + offset
    print "gain = 37-power + offset = [%s]" % Ggain

    #================ get VVA word ===============
    newCmd1 = sendModifylineToFRmon(dlGainSeqfile,32,"G1gain",str(Ggain),log)
    #print newCmd1
    sendfrmon(tnFR,newCmd1,log)
    wait(5)
    vva1 = sendlineToFRmon(dlGainSeqfile,35,log)
    #print "vva1 is [%s]" % vva1
    vva2 = re.search(r'\d{4}', vva1)
    vvaWord = int(vva2.group(0))
    print "vvaWord is [%s]" % vvaWord
    #=============================================

    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,36,37,log)

    #=========== get RFchain1 temperature ========
    temp1 = sendlineToFRmon(dlGainSeqfile,38,log)
    print "temp1 is [%s]" % temp1

    temp2 = re.search(r'(\d{2})\.(\d+)', temp1)
    rfChainTemp = float(temp2.group(0))
    print "rfChainTemp is [%s]" % rfChainTemp
    #=============================================
    
    wait(3)
    # destory the carrier(1tx+1rx)
    sendfewlinetoFRmonandCheckAck(dlGainSeqfile,41,44,log)
    wait(5)
    logit(("[End] the TX calibration for []Mhz is done." % freq_tx),log)
    calibResult[i] = [Ggain,tx_mark[i],rfChainTemp,vvaWord]
print calibResult
    
