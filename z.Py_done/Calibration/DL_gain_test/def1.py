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

def sendlineToFRmon(file,linenum,log,FRtn):
    lineContent = getlineContent(file,linenum)
    cmd = lineContent[0]
    ack = sendfrmon(FRtn,cmd,log)
    return ack

def modifylinetoStr(file,linenum,origWord,replaceWord,log):
    lineContent = getlineContent(file,linenum)
    cmd = lineContent[0]
    newCmd = cmd.replace(origWord,replaceWord)
    return newCmd

def sendfewlinetoFRmonandCheckAck(file,beginlineNum,endlineNum,log,FRtn):
    for i in range(beginlineNum,endlineNum+1):
        lineContent = getlineContent(file,i)
        cmd = lineContent[0]
        ea = lineContent[1]
        expectAck = ea.strip()
        realAck = sendfrmon(FRtn,cmd,log)
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
        fsvPre = ["*RST","INIT:CONT OFF","SYST:DISP:UPD ON","INST LTE","CONF:DL:BW BW" + band,"POW:AUTO2 ON","DISP:TRAC:Y:RLEV:OFFS " + inCableLoss,"CALC2:FEED 'SPEC:ACP'","FREQ:CENT "+ freq +"MHz",]
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