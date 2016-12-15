# coding: UTF-8

a = raw_input("随便输入一个整数,我来分析分析:")
b = [2,3,7]  # 遍历的目录
for i in range(3):
    c = (int(a) % b[i]) == 0
    if c:
        print "这个数可以被%d整除" % b[i]