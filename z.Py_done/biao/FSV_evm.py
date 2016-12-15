################################################################################
# @version               v1
# @date                  2015-07-29
# @author                Yunpeng
#
# Original author        Yunpeng
#
# Copyright 2014 Nokia Networks. All rights reserved.
################################################################################

import re
import os
import sys
import telnetlib
import time
#from operator import itemgetter

HOST = "192.168.1.2"           #connect to FSV
#list_FsvCmd = ["*RST","INIT:CONT OFF","SYST:DISP:UPD ON","INST LTE","FREQ:CENT 2140 MHz","CONF:DL:BW BW5_00","POW:AUTO2 ON","DISP:TRAC:Y:RLEV:OFFS 42"]
#I_NumFsv = len(list_FsvCmd)

def build_Matrix(x,y,ele=0):
    N=[]
    F=[]
    for i in range(x):
        for j in range(y):
            F.append(ele)
        N.append(F)
        F=[]
    return N

def func_TxEvm(s_FsvHost,s_Freq,s_BandWidth,s_CableLoss,i_TestTimes,i_TestGap):
    logname = "tx_evm"
    dict_SupportBands = {'1.4':'1_40', '3':'3_00', '5':'5_00','10':'10_00','15':'15_00','20':'20_00'}
    s_BW = dict_SupportBands[s_BandWidth]
    list_FsvCmd = ["*RST","INIT:CONT OFF","SYST:DISP:UPD ON","INST LTE","FREQ:CENT "+s_Freq+"MHz","CONF:DL:BW BW"+s_BW,"POW:AUTO2 ON","DISP:TRAC:Y:RLEV:OFFS "+s_CableLoss]
    i_NumFsvCmd = len(list_FsvCmd)
    list_Results = build_Matrix(int(i_TestTimes),3)
    of = open('%s.log' % logname, 'w')
    list_EvmCmd = ["FETC:SUMM:EVM?","FETC:SUMM:EVM:ALL:MAX?","FETC:SUMM:EVM:ALL:MIN?"]
    i_NumEvmCmd = len(list_EvmCmd)
    list_EvmHint = ["average","maximum","minimum"]

    # prepare FSV for test
    tn = telnetlib.Telnet(s_FsvHost, port=5025)
    for i in range(0,i_NumFsvCmd):
        tn.write(list_FsvCmd[i] + "\n")
        time.sleep(3)
        print("==> SEND : %s " % list_FsvCmd[i])
        of.write('==> SEND : %s \r\n' % str(list_FsvCmd[i]) )

    ################ begin of Tx_Evm  #################
    print("go to summary windows")
    tn.write("CALC2:FEED 'STAT:ASUM'\n") #go to summary windows
    of.write("==> SEND : CALC2:FEED 'STAT:ASUM' ,go to summary windows \r\n")
    time.sleep(1)

    tn.write("INIT:CONT OFF\n") #turn to run single mode
    of.write("==> SEND : INIT:CONT OFF ,turn to run single mode \r\n \r\n===== begin test ===== \r\n \r\n")
    time.sleep(1)

    for i in range(0,int(i_TestTimes)):
        print("query TxEvm and save results for (%s/%s) time." % ((i+1),i_TestTimes))
        tn.write("INIT;*WAI\n") # execute test for one time
        of.write("==> SEND : INIT;*WAI ,execute test for one time \r\n \r\n")
        time.sleep(3)
        of.write('TxEvm test result for %s time : \r\n' % (i+1) )

        for j in range(0,i_NumEvmCmd):
            tn.write(list_EvmCmd[j]+"\n") # ask for EVM-all result
            of.write("    ==> SEND : "+list_EvmCmd[j]+",ask for EVM-all "+list_EvmHint[j]+"result \r\n \r\n")
            time.sleep(1)
            temp = tn.read_very_eager()
            list_Results[i][j] = temp
            of.write('    TxEvm_ALL_%s is: %s\r\n' % (str(list_EvmHint[j]),str(list_Results[i][j])) )

        if list_Results[i] == [0,0,0]:
            print "==== get TxEvm result error!! ===="
            of.write("=== data list is all 0,get TxEvm result error!! \r\n")
            break
        time.sleep(int(i_TestGap))
    ################ end of TxEvm  #################

    print "===== End test =====\r\n"
    return list_Results

J = func_TxEvm(HOST,"2120","20","42.4","2","4")
print ("the last results is:\r\n    %s" % str(J))