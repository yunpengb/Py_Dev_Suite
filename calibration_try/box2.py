'''
file = "D:\\byp\\TOPIC\\DL_gain\\DL_gain_fenxi\\cmdset\\FHEI_1842.5.csv"
nu = 10
a = lineContent(file,nu)
#print a
a1 = a.split(',')
#print "@_@Cmd is:[%s]" % a1[0]
#print "@_@ExpectAck is:[%s]" % removeEmptyStr(a1[1])
cmd = a1[0]
ac1 =a1[1]
ac2 = ac1.strip()
expectAck = ac2.rstrip('>')

result = checkfrmonDone(tnFR,cmd,expectAck)
if result :
    #print result
    print "Yes,result is done!"
    print "true end"
else:
    #print result
    print 'sth is wrong!'
    sys.exit("================ ack is not expect,stop! ================")
    print "false end"

print "see end"
'''