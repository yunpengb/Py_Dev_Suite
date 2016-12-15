# coding:UTF-8

def addint(a,b):
    return int(a)+int(b)
    
def askADD(hint):
    ht = str(hint)
    print ht,"部分："
    a1 = raw_input("加法:请给我一个整数:")
    a2 = raw_input("加法:请再给我一个整数:")
    c = addint(a1,a2)
    print "%s部分的结果是%d\n" % (ht,c)

d = askADD('a')
d = askADD('b')
