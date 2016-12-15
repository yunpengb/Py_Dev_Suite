# coding: UTF-8

a = ["a","b","c"]
for i,j in enumerate(a):
    print i,j
#---------------------------------    
print "----------"   
b = ("a","b","c")
for i,j in enumerate(b):
    print i,j
#---------------------------------
print "----------"   
c = {"a":4,"b":5,"c":6} # 不推荐使用
for i,j in enumerate(c):
    print i,j
#---------------------------------
print "----------"   
d = "cat1"
for i,j in enumerate(d):
    print i,j   