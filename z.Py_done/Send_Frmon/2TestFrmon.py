#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

################################################################################
# @script name   send FRMON cmd to telnet port and get results in csvlog
# @version               v1
# @date                  2015-10-15
# @author                Yunpeng
# @draft                 Yunpeng
# 
# @Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import sys
import telnetlib,subprocess,re
import argparse,os
import time,random
import xlrd
from ftplib import FTP

def readconfig(configfile):
    paraD = {}
    parameter = []
    value = []
    #	Load file with config parameters
    file1 = open(configfile, 'r')
    try:
		lines1 = file1.readlines()
    finally:
        file1.close()
    
    for line in lines1:
        linedata = line.split("=")
        key = linedata[0]
        val = linedata[1].strip()
        parameter.append(key)
        value.append(val)
        #print ('Get parameter : %s = %s' % (key,val))
        paraD.setdefault(key,val)
    #print paraD
    return paraD

def ping(ip):
    COUNT = '10'
    TIMEOUT = '6'
    p = subprocess.Popen(["ping.exe",ip,'-n',COUNT,'-w',TIMEOUT],stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)    

    data = p.stdout.read()
    print data
    
    re_packets = re.compile('.*= ([0-9]+).*= ([0-9]+).*= ([0-9]+).*\(([0-9]+%).*')
    #print re_packets.findall(data)
    b = re_packets.findall(data)
    #print b[0][3]
    percentStr = b[0][3]
    print percentStr.find('%')
    endNum = percentStr.find('%')
    percentNum = int(percentStr[0:endNum])

    if percentNum <= 20 :
        result = True
    else :
        print "ping is not OK!!"
        #print re_packets
        result = False
    return result    
    
def ftp_up(host,port,filename = "data_LTE5.bin"):
    ftp=FTP()
    ftp.set_debuglevel(2)#
    ftp.connect(host,port)#
    ftp.login('','')#
    #print ftp.getwelcome()#
    #ftp.cwd('xxx/xxx/') #
    bufsize = 1024#
    file_handler = open(filename,'rb')#
    ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize)#
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    print "ftp up OK"    
    
def readCmd(xlsfile):
    temp = ""
    pool = []
    Workbook = xlrd.open_workbook(xlsfile)
    worksheet = Workbook.sheet_by_name("FRMON")
    
    global nrows
    nrows = worksheet.nrows
    print "there are %s rows in xls" % nrows
    ncols = worksheet.ncols
    print "there are %s cols in xls" % ncols
    
    for i in range(1,nrows):
        rowdata = worksheet.row_values(i)
        #print rowdata
        for i in range(len(rowdata)):
            rowdata[i] = str(rowdata[i])
        pool.append(rowdata)
    return pool

def creatEmptyCSV(name):
    s = "\n"
    f = open(name,'w')
    f.write(s)
    f.close()

def list2strWithComma(list):
    for i in range (len(list)):
        list[i] = str(list[i])
    a = ",".join(list)
    return a
    
def addline2csv(origcsv,Datalist):
    "new data need be a list(one grade)"
    csvfile = open(origcsv,'a+')
    new = list2strWithComma(Datalist)
    newline = new + "\n"
    csvfile.write(newline)
    csvfile.close()    

def maketimestamp():
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
    return timestamp
    
def sendCmdSet(cmdset):
    #	Open telent connection to RFM
    ack = []
    match=[]
    resultAll=[]
    tnMark = False
    
    for i in range(len(cmdset)):
        tag = cmdset[i][0]
        line = cmdset[i][1]
        expectAck0 = cmdset[i][2]
        expectAck = expectAck0.strip()
        
        if tnMark == True:
            print ('frmon testing...[%s]' % i)
        elif tnMark == False:
            pingMark = False
            while(not pingMark):
                time.sleep(30)
                print 'judge if ping to 69 is OK ...'
                pingMark = ping('192.168.255.69')
            print 'ping to unit is OK'
            tnMark = True
            try:
                tn = telnetlib.Telnet(frmonIP_1, port, TIMEOUT)
                print "connect to %s done!" % frmonIP_1
                print ('frmon testing...[%s]' % i)
            except:
                try:
                    tn = telnetlib.Telnet(frmonIP_2, port)
                except:	
                    print 'Unable to connect frmon'
                    time.sleep(1)
                    sys.exit(0)
        
        if tag == "sleep":
            sec = float(line)
            print "========== wait for %s seconds ===========" % sec
            time.sleep(sec)
            ack.append("sleep for %s seconds" % str(sec))
            match.append("-")
            continue
        elif tag == 'ftpin' and ('data_LTE5.bin' in line):
            ftp_up('192.168.255.69','21','data_LTE5.bin')
            ack.append('upload done~')
            match.append("-")
            time.sleep(3)
        elif tag == 'reset':
            cmd = str(line)
            #print "==> FRMON input: [%s]" % cmd
            tn.write(cmd+"\n")
            tnMark = False
            ack.append('reset send')
            match.append("-")
        else:
            cmd = str(line)
            #print "==> FRMON input: [%s]" % cmd
            tn.write(cmd+"\n")
            ra = tn.read_until("==>")
            rb = tn.read_until("\n>")
            r = ra + rb
            r0 = r.strip()
            r1 = r0.strip(">")
            r2 = r1.strip()
            #print "<== FRMON output: [%s]" % r2
            ack.append(r2)
            if r2 == expectAck :
                match.append("Match")
            else:
                match.append("Not match")
        time.sleep(1)
    tn.close()
    resultAll.append(ack)
    resultAll.append(match)
    return resultAll
          
def saveCsvlog(cmdset,resultAll,logtag):
    firstline = ["Tag","Frmon_Cmd","Expect_Ack","Real_Ack","Do it Match Expect?"]
    timestat = maketimestamp()
    logName = logtag + "_" + timestat + ".csv"
    creatEmptyCSV(logName)
    addline2csv(logName,firstline)
    for i in range(len(cmdset)):
        line = []
        line = cmdset[i]
        line.append(resultAll[0][i])
        line.append(resultAll[1][i])
        addline2csv(logName,line)

configfile = "config.ini"
xlsfile = "cmd.xls"
parameter = readconfig(configfile)
logTag = parameter["logtagname"]
frmonIP_1 = parameter["frmonIP_1"]
frmonIP_2 = parameter["frmonIP_2"]
port = int(parameter["port"])
TIMEOUT = int(parameter["timeout"])
        
cmdpool = readCmd(xlsfile)
ack = sendCmdSet(cmdpool)
saveCsvlog(cmdpool,ack,logTag)