# coding:UTF-8

def addint(a,b):
    return int(a)+int(b)
    
def askADD(hint):
    ht = str(hint)
    print ht,"���֣�"
    a1 = raw_input("�ӷ�:�����һ������:")
    a2 = raw_input("�ӷ�:���ٸ���һ������:")
    c = addint(a1,a2)
    print "%s���ֵĽ����%d\n" % (ht,c)

d = askADD('a')
d = askADD('b')
