################################################################################
# @version               v1
# @date                  2015-07-29
# @author                Yunpeng
#
# Original author        Yunpeng
#
# Copyright 2014 Nokia Networks. All rights reserved.
################################################################################

#explanation:   this script will remote control FSV get into LTE mode,and get TXpower and ACLR value to log file
#precondition: connect FSV and PC with ethernet cable and set them to same network segment.eg:  FSV:192.168.1.2;  PC:192.168.1.1 (can ping to each other)
#how to use:    edit variables below at the begining of script before run it

import re
import os
import sys
import telnetlib
import time

HOST = "192.168.1.2" #IP of FSV
freq = "2140"     # unit in MHz,support 2~6Ghz
band = "20"       # unit in MHz,support 1.4\3\5\10\15\20 Mhz(in LTE mode)
cableloss = "42.4" # unit in db
times = "5"     # test times(if test n times,will get n group of value in log file)
gap = "10"      #unit in second,the wait time between two test

def build_Matrix(x,y,ele=0):
    N=[]
    F=[]
    for i in range(x):
        for j in range(y):
            F.append(ele)
        N.append(F)
        F=[]
    return N

def func_TxAclr(s_FsvHost,s_Freq,s_BandWidth,s_CableLoss,i_TestTimes,i_TestGap):
    logname = "aclr"
    dict_SupportBands = {'1.4':'1_40', '3':'3_00', '5':'5_00','10':'10_00','15':'15_00','20':'20_00'}
    s_BW = dict_SupportBands[s_BandWidth]
    list_FsvCmd = ["*RST","INIT:CONT OFF","SYST:DISP:UPD ON","INST LTE","FREQ:CENT "+s_Freq+"MHz","CONF:DL:BW BW"+s_BW,"POW:AUTO2 ON","DISP:TRAC:Y:RLEV:OFFS "+s_CableLoss]
    i_NumFsvCmd = len(list_FsvCmd)
    list_Results = build_Matrix(int(i_TestTimes),5)
    of = open('%s.log' % logname, 'w')

    # prepare FSV for test
    tn = telnetlib.Telnet(s_FsvHost, port=5025)
    for i in range(0,i_NumFsvCmd):
        tn.write(list_FsvCmd[i] + "\n")
        time.sleep(3)
        print("==> SEND : %s " % list_FsvCmd[i])
        of.write('==> SEND : %s \r\n' % str(list_FsvCmd[i]) )

    ################ begin of ALCR  #################
    print("go to ACLR windows")
    tn.write("CALC2:FEED 'SPEC:ACP'\n") #go to alcr windows
    of.write("==> SEND : CALC2:FEED 'SPEC:ACP' ,go to aclr windows \r\n")
    time.sleep(1)

    tn.write("INIT:CONT OFF\n") #turn to run single mode
    of.write("==> SEND : INIT:CONT OFF ,turn to run single mode \r\n \r\n ===== begin test ===== \r\n \r\n")
    time.sleep(1)

    for i in range(0,int(i_TestTimes)):
        print("query ACLR and save results for (%s/%s) time." % ((i+1),i_TestTimes))
        tn.write("INIT;*WAI\n") # execute test for one time
        of.write("    ==> SEND : INIT;*WAI ,execute test for one time \r\n")
        time.sleep(3)
        tn.write("CALC1:MARK:FUNC:POW:RES?\n") # ask for aclr result
        of.write("    ==> SEND : CALC1:MARK:FUNC:POW:RES? ,ask for aclr result \r\n \r\n")
        time.sleep(1)
        temp = tn.read_very_eager()

        list_Results[i] = temp.split(',')
        of.write('ACLR test result for %s time : \r\n Out Power is: %s\r\n  ACLR_%sM_lower is:%s\r\n  ACLR_%sM_upper is:%s\r\n  ACLR_%sM_lower is:%s\r\n  ACLR_%sM_upper is:%s\r\n' % ((i+1),str(list_Results[i][0]),band,str(list_Results[i][1]),band,str(list_Results[i][2]),band,str(list_Results[i][3]),band,str(list_Results[i][4]) ) )
        if list_Results[i] == [0,0,0,0,0]:
            print "==== get aclr result error!! ===="
            of.write("=== data list is all 0,get aclr result error!! \r\n")
            break
        time.sleep(int(i_TestGap))
    ################ end of ALCR  #################

    print "===== End test =====\r\n"
    time.sleep(1)
    of.close()
    return list_Results

J = func_TxAclr(HOST,freq,band,cableloss,times,gap)
print ("the last results is:\r\n    %s" % str(J))
