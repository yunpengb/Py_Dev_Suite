# coding: UTF-8

a = raw_input("�������һ������,������������:")
b = [2,3,7]  # ������Ŀ¼
for i in range(3):
    c = (int(a) % b[i]) == 0
    if c:
        print "��������Ա�%d����" % b[i]