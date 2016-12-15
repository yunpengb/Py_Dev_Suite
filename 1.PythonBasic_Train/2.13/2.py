a = None
b = 1
c = 1.1
d = True
e = "Jobs"
f = (1,1,"Bill Gates")

print id(b)
b = 10
print b
print id(b),"\n--------------"
#-------------
print id(b)
b = 11
print b
print id(b),"\n--------------"
#-------------
print id(d)
d = False
print d
print id(d),"\n--------------"
#-------------
print id(e)
e = "AQ"
print e
print id(e),"\n--------------"
#-------------
print id(f)
f = (1,1,2)
print f
print id(f),"\n--------------"