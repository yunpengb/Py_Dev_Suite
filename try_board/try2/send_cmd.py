import re
import os
import sys
import telnetlib
import time
from operator import itemgetter

HOST = "192.168.1.131"           #connect Telnet
tn = telnetlib.Telnet(HOST, port=200)
result = tn.read_until(">")
print(result)

with open("command.txt", "r") as caseFileObject:   #open test case file
    caselines = caseFileObject.readlines()
    for caseline in caselines:
            tn.write(caseline)
            print(caseline)
            result = tn.read_until('>',1)
            print(result)
tn.close()