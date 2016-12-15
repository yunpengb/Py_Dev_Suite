# coding=utf-8

import serial
import time

def setTout(t):
    print "Old Timeout is:[%s]" % po1.getTimeout() 
    po1.setTimeout(t)
    print "New Timeout is:[%s]" % po1.getTimeout() 

def sendShell(sp,cmd):
    sp.write(cmd+"\n")
    print "send shell cmd:[%s]" % cmd
    str = sp.readall()
    return str

def shell_io(sp,cmd,sleepTime):
    str = sendShell(sp,cmd) 
    print str
    time.sleep(sleepTime)
    
po1 = serial.Serial('com1',115200) 
timeStart = time.time() 
portnow = po1.portstr         
print "COM port now is:[%s]" % portnow
setTout(5)

shell_io(po1,"hwid",2)

shell_io(po1,"build_info",2)

shell_io(po1,"rfctrl txStat",2)

po1.close()

