# coding: utf-8

a = raw_input("Please input a number:")

if int(a) % 2 == 0:
    print "[%s]\n ����2�������� " % a
elif int(a) % 3 == 0:
    print "[%s]\n ����3��������" % a
elif int(a) % 7 == 0:
    print "[%s]\n ����7��������" % a
else:
    print "ʲôҲ��˵"