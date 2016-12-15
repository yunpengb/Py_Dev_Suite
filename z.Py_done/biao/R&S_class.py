################################################################################
# @version               v1
# @date                  2015-08-10
# @author                Yunpeng
#
# Original author        Yunpeng
# 
# Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import os
import sys
import telnetlib
import time
import subprocess    
import re

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
        print re_packets
        result = False
    return result
    
def build_Matrix(x,y,ele=''):
	N=[]
	F=[]
	for i in range(x):
		for j in range(y):
			F.append(ele)
		N.append(F)
		F=[]
	return N

class RS_Meter(object):
    'FSV and SMU remote control and results query'
    global fsvtn,fsvlog,smutn,smulog
    port = 5025
    fsvlogname = "fsvRecord"
    smulogname = "smuRecord"
    fsvtn = telnetlib.Telnet(fsvip, port)
    smutn = telnetlib.Telnet(smuip, port)
    fsvlog = open('%s.log' % fsvlogname, 'w')
    smulog = open('%s.log' % smulogname, 'w')
    
    def _int_(self,fsvip,smuip):
        'make sure FSV and SMU is ready'
        pfsv = ping(fsvip)
        psmu = ping(smuip)
        
        if pfsv:
            print 'FSV is ping OK,ready~'
        else:
            print 'FSV can not pinging! pls check connection to FSV'
        if psmu:
            print 'SMU is ping OK,ready~'
        else:
            print 'SMU can not pinging! pls check connection to SMU'
        return pfsv*psmu
            
    def externalClock(self):
        fsvextRel = ["ROSC:SOUR EXT","ROSC:EXT:FREQ 10"]
        smuextRel = ["ROSC:SOUR EXT","ROSC:EXT:FREQ 10MHz"]
        for i in range(0,len(fsvextRel)):
            fsvtn.write(fsvextRel[i] + "\n")
            time.sleep(2)
            fsvlog.write('[justifyClock] ==> SEND : %s \r\n' % str(fsvextRel[i]) )
        print 'FSV is using external 10Mhz clock now!'
        fsvlog.write('[justifyClock] FSV is using external 10Mhz clock now! \r\n')
        for i in range(0,len(smuextRel)):
            smutn.write(smuextRel[i] + "\n")
            time.sleep(2)
            smulog.write('[justifyClock] ==> SEND : %s \r\n' % str(smuextRel[i]) )
        print 'SMU is using external 10Mhz clock now!'
        smulog.write('[justifyClock] smu is using external 10Mhz clock now! \r\n')
        
    def fsvPrepare(self,bandwidth):
        'make FSV ready in LTE mode'
        dict_SupportBands = {'1.4':'1_40', '3':'3_00', '5':'5_00','10':'10_00','15':'15_00','20':'20_00'}
        band = dict_SupportBands[bandwidth]
        fsvPre = ["*RST","INIT:CONT OFF","SYST:DISP:UPD ON","INST LTE","CONF:DL:BW BW"+band,"POW:AUTO2 ON"]
        
        for i in range(0,len(fsvPre)):
            fsvtn.write(fsvPre[i] + "\n")
            time.sleep(2)
            print("==> SEND : %s " % fsvPre[i])
            fsvlog.write('[FsvPrepare] ==> SEND : %s \r\n' % str(fsvPre[i]) )
        print 'FSV is prepared in LTE mode!'
        fsvlog.write('[FsvPrepare] FSV is prepared in LTE mode!')

    def fsvAclr(self,freq,carrierband,cableloss,testtimes='3',testgap='3'):
        'input necessary parameter and query aclr value'
        aclrRusults = build_Matrix(int(testtimes)+1,8)
        aclrpre = ["CALC2:FEED 'SPEC:ACP'","FREQ:CENT "+freq+"MHz","DISP:TRAC:Y:RLEV:OFFS "+cableloss]
        
        for i in range(0,len(aclrpre)):
            fsvtn.write(aclrpre[i] + "\n")
            time.sleep(2)
            print("==> SEND : %s " % aclrpre[i])
            fsvlog.write('[FsvAclr] ==> SEND : %s \r\n' % str(aclrpre[i]) )
        doubleband = str(2*int(carrierband))
        aclrRusults[0] = ["TxAclr","carrierWidth(Mhz)","freq(Mhz)","TxPower(dbm)","Aclr_"+carrierband+"M_lower(db)","Aclr_"+carrierband+"M_upper(db)","Aclr_"+doubleband+"M_lower(db)","Aclr_"+doubleband+"M_lower(db)"]
        for i in range(1,int(testtimes)+1):
            print("query ACLR and save results for (%s/%s) time." % ((i+1),testtimes))
            fsvtn.write("INIT;*WAI\n") # execute test for one time
            fsvlog.write("[FsvAclr]    ==> SEND : INIT;*WAI ,execute test for one time \r\n")
            time.sleep(2)
            fsvtn.write("CALC1:MARK:FUNC:POW:RES?\n") # ask for aclr result
            fsvlog.write("[FsvAclr]    ==> SEND : CALC1:MARK:FUNC:POW:RES? ,ask for aclr result \r\n \r\n")
            time.sleep(1)
            temp = fsvtn.read_very_eager()
            aclrRusults[i][1] = carrierband
            aclrRusults[i][2] = freq
            data = temp.split(',')
            for j in range(5):
                aclrRusults[i][j+3] = data[j]
            
            fsvlog.write('[FsvAclr] ACLR test result for %s time : \r\n Out Power is: %s\r\n  ACLR_%sM_lower is:%s\r\n  ACLR_%sM_upper is:%s\r\n  ACLR_%sM_lower is:%s\r\n  ACLR_%sM_upper is:%s\r\n' % ((i),str(aclrRusults[i][3]),band,str(aclrRusults[i][4]),band,str(aclrRusults[i][5]),band,str(aclrRusults[i][6]),band,str(aclrRusults[i][7]) ) )
            
            if aclrRusults[i] == ['']*8:
                print "==== get aclr result error!! ===="
                fsvlog.write("[FsvAclr] === data list is all 0,get aclr result error!! \r\n")
                break
            time.sleep(int(testgap))
        return aclrRusults
        
    def fsvEvm(self,freq,carrierband,cableloss,testtimes='3',testgap='3'):
        'set freq and cableloss,query evm value'
        evmpre = ["FREQ:CENT "+freq+"MHz","DISP:TRAC:Y:RLEV:OFFS "+cableloss,"CALC2:FEED 'STAT:ASUM'"]
        evmCmd = ["FETC:SUMM:EVM?","FETC:SUMM:EVM:ALL:MAX?","FETC:SUMM:EVM:ALL:MIN?"]
        evmResults = build_Matrix(int(testtimes)+1,6)
        list_EvmHint = ["average","maximum","minimum"]
        
        for i in range(0,len(evmpre)):    # prepare FSV for test
            fsvtn.write(evmpre[i] + "\n")
            time.sleep(2)
            print("==> SEND : %s " % evmpre[i])
            fsvlog.write('[FsvEvm] ==> SEND : %s \r\n' % str(evmpre[i]) )
        
        evmResults[0] = ["TxEvm","carrierWidth(Mhz)","freq(Mhz)","TxEvm_average(%)","TxEvm_max(%)","TxEvm_min(%)"]
        for i in range(1,int(testtimes)+1):
            print("query TxEvm and save results for (%s/%s) time." % ((i+1),testtimes))
            fsvtn.write("INIT;*WAI\n") # execute test for one time
            fsvlog.write("[FsvEvm] ==> SEND : INIT;*WAI ,execute test for one time \r\n \r\n")
            time.sleep(2)
            fsvlog.write('[FsvEvm] TxEvm test result for %s time : \r\n' % (i+1) )
            
            for j in range(0,len(evmCmd)):
                fsvtn.write(evmCmd[j]+"\n") # ask for EVM-all result
                fsvlog.write("[FsvEvm]     ==> SEND : "+evmCmd[j]+",ask for EVM-all "+list_EvmHint[j]+"result \r\n \r\n")
                time.sleep(1)
                temp = fsvtn.read_very_eager()
                
                evmResults[i][1] = carrierband
                evmResults[i][2] = freq
                data = temp.split(',')
                for j in range(3):
                    evmResults[i][j+3] = data[j]
                    fsvlog.write('[FsvEvm]     TxEvm_ALL_%s is: %s\r\n' % (str(list_EvmHint[j]),str(evmResults[i][j+3])) )
            
            if evmResults[i] == ['']*6:
                print "==== get TxEvm result error!! ===="
                fsvlog.write("[FsvEvm] === data list is all 0,get TxEvm result error!! \r\n")
                break
            time.sleep(int(testgap))
        return evmResults
        
    def smuPrepare(self):
        'make smu ready for test'
        smupre = ["*RST","ROSC:SOUR EXT","ROSC:EXT:FREQ 10MHz","ROSC:EXT:SBAN NARR"]
        
        for i in range(0,len(smupre)):
            smutn.write(smupre[i] + "\n")
            time.sleep(2)
            print("==> SEND : %s " % smupre[i])
            smulog.write('[smuPrepare] ==> SEND : %s \r\n' % str(smupre[i]) )
        print "===== End test =====\r\n"
        smulog.write("[smuPrepare] ===== End test =====\r\n")
        return
    
    def smuSetARB(self,wavePath,bandwidth,modulation):
        'set arb file ,and ARB On'
        arbcmd = ["BB:ARB:WAV:SEL '"+wavePath+"\\"+"LTE_UL_4GMax_PN18_"+bandwidth+"_"+modulation+"'","BB:ARB:TRIG:SEQ AUTO","BB:ARB:STAT ON"]
        for i in range(0,len(arbcmd)):
            smutn.write(arbcmd[i] + "\n")
            time.sleep(2)
            print("==> SEND : %s " % arbcmd[i])
            smulog.write('[smuSetARB] ==> SEND : %s \r\n' % str(arbcmd[i]) )
        return
        
    def smu_freqandOn(self,freq,offset,rfoutlev):
        'set signal freq and RF On'
        freqcmd = ["FREQ "+freq+"Mhz","POW:OFFS "+offset,":POW "+rfoutlev,"OUTP ON"]
        for i in range(0,len(freqcmd)):
            smutn.write(freqcmd[i] + "\n")
            time.sleep(2)
            print("==> SEND : %s " % freqcmd[i])
            smulog.write('[smu_freqandOn] ==> SEND : %s \r\n' % str(freqcmd[i]) )
        return
            
    def fsvclean(self):
        'clean fsv stuff'
        fsvlog.close()
        fsvtn.close()
        return
        
    def smuclean(self):
        'clean smu stuff'
        smulog.close()
        smutn.close()
        return
    
    def calcCableloss(freq,outlev):
        cableloss = [-100.0]*5
        sendSinglewave = ["*RST","FREQ "+freq+"Mhz",":POW "+outlev,"OUTP ON"]
        readPowerpre = ["*RST","CALC:MARK:AOFF","CALC:MARK1 ON","CALC:MARK:X "+freq+"MHz"]
        
        for i in range(0,len(sendSinglewave)):
            fsvtn.write(sendSinglewave[i] + "\n")
            time.sleep(2)
            fsvlog.write('[calcCablelossSMU] ==> SEND : %s \r\n' % str(sendSinglewave[i]) )
        print 'SMU is sending singlewave now!'
    
        for i in range(0,len(readPowerpre)):
            fsvtn.write(readPowerpre[i] + "\n")
            time.sleep(2)
            fsvlog.write('[calcCablelossFSV] ==> SEND : %s \r\n' % str(readPowerpre[i]) )
        print 'FSV has readed the power!'
        for i in range(0,5):
            fsvtn.write("CALC:MARK1:Y?\n") # ask for power result
            fsvlog.write("[calcCablelossFSV]    ==> SEND : CALC:MARK1:Y? ,ask for power result \r\n \r\n")
            time.sleep(1)
            cableloss[i] = fsvtn.read_very_eager()
            time.sleep(1)
        loss = sum(cableloss)/5
        return loss