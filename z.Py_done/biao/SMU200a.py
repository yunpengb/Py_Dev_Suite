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

HOST = "192.168.1.3"           #connect to FSV

def func_RxSmuEvmSet(s_SmuHost,s_Freq,s_BandWidth,s_OffSet,s_Modulation,s_wavePath,s_RfOutLev):
    logname = "rx_Smu"
    band = ["1","3","5","10","15","20"]
    list_SmuCmd = ["*RST","ROSC:SOUR EXT","ROSC:EXT:FREQ 10MHz","ROSC:EXT:SBAN NARR","BB:ARB:WAV:SEL '"+s_wavePath+"\\"+"LTE_UL_4GMax_PN18_"+s_BandWidth+"_"+s_Modulation+"'","FREQ "+s_Freq+"Mhz","BB:ARB:TRIG:SEQ AUTO","BB:ARB:STAT ON","POW:OFFS "+s_OffSet,":POW "+s_RfOutLev,"OUTP ON"]
    i_NumSmuCmd = len(list_SmuCmd)
    of = open('%s.log' % logname, 'w')

    if s_BandWidth in band:

        # prepare SMU for test
        tn = telnetlib.Telnet(s_SmuHost, port=5025)
        for i in range(0,i_NumSmuCmd):
            tn.write(list_SmuCmd[i] + "\n")
            time.sleep(3)
            print("==> SEND : %s " % list_SmuCmd[i])
            of.write('==> SEND : %s \r\n' % str(list_SmuCmd[i]) )
        print "===== End test =====\r\n"
        of.write("===== End test =====\r\n")
    else:
        print "input band not support(no matching IQpro waveform)!"
        of.write("input band not support(no matching IQpro waveform)!")
    time.sleep(1)
    of.close()
    return

print "begin:\r\n"
func_RxSmuEvmSet(HOST,"1960","15","14.14","QPSK","D:\\smu_arb","-50")