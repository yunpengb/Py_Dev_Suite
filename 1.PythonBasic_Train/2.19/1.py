x = 1

def a():
    x =2
    def b():
        global x
        x = 3
        print "locals",x
    b()
    print "enclosing function locals",x
a()
print "global",x