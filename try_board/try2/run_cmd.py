import os
import re

dir = "FRM35.09.R01"
cmd = ["C:","cd C:\\Temp_a\\" + dir + "\\C_Element\\SE_RFM\\SS_REL3\\RnD","dir"]

# execute command, and return the output
def runCmd(cmd):
    global r
    r = os.popen(cmd)
    text = r.read()
    return text

def closeCmd():
    r.close()

# for i in range(len(cmd)):
    # result = runCmd(cmd[i])
    # print ("-->Cmd send: %s" % cmd[i])
    # print ("<--Cmd back: %s" % result)
# closeCmd()

cc = cmd[0]
for i in range(1,len(cmd)):
    cc = cc + "&&" + cmd[i]
result = runCmd(cc)


print ("-->Cmd send: %s" % cc)
print ("<--Cmd back: %s" % result)

#pattern = r"^FRM-.*?LAR\n$"
pattern = r"FRM-\w*"
res = re.findall(pattern,result)
print res