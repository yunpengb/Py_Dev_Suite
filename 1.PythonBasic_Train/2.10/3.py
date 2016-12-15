a = {"Xiaoming":180,"HanMeiMei":170,"Jobs":175,"YaoMing":226,"aQ":150}
b = {1:2,"a1":"b1","a2":[1,2],(1,2):[3,4]}

print a.keys()
print a.values()
print a.items()
print "==========\n",

#----------change element letter---------------
print a.keys()[0]
print a.keys()[0].upper()
print a.keys()[0].lower()

c = {}
for i in range(len(a)):
    k = a.keys()[i]
    key = k.lower()
    c[key] = a[k]
print c
c.clear()
print c