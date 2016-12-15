a = {"Xiaoming":180,"HanMeiMei":170,"Jobs":175,"YaoMing":226,"aQ":150}
b = {1:2,"a1":"b1","a2":[1,2],(1,2):[3,4]}

print a.keys()
print a.values()
print a.items()
print "==========\n",
#----------sort out keys-----------
d = a.keys()
d.sort()
print d
d.reverse()
print d
print "==========\n",
#----------sort out values---------
d = a.values()
d.sort()
print d
d.reverse()
print d
print "==========\n",
