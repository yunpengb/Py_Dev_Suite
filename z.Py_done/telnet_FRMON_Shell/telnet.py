import telnetlib

unitIP = "192.168.255.69"
FRMport = 200
tnFR = telnetlib.Telnet(unitIP, FRMport)

tnFR.write("frmon do")
tnshell.write("flash -u " + DCFnow + " DCF.zip\n")
logit("send: flash -u %s DCF.zip" % DCFnow)
time.sleep(10)