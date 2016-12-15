b = [1,"HAHA",3,4,5]
a = 2
for i in range(len(b)):
    try:
        print a + b[i], # try add a C
    except IOError:
        print "[+_+:----IOError happen----]"
    except TypeError:
        print "[+_+:----TypeError happen----]"
    except NameError:
        print "[+_+:----NameError happen----]"
    else:
        print "[^_^:no ERR ]",
    finally:
        print "<end>"
    
    