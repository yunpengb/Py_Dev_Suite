g = [1,1,"Bill Gates"]
h = {"YaoMing":226,"Jobs":188}
i = {1,2,"Bill Gates"}

print id(g)
g.append(2)
print g
print id(g),"\n--------------"
#-----------------------
print id(h)
h["AQ"]=150
print h
print id(h),"\n--------------"
#-----------------------
print id(i)
i.add("cat")
print i
print id(i)