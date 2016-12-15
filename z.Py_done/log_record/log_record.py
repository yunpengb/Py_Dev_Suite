


#@@~~~~~~~~~~~~~~~~~ creat log for every single run time ~~~~~~~~~~~~~~~~~~~
timestamp = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
logmark = "log_" + timestamp
currentlogDir = logdir + "\\" +logmark
os.mkdir(currentlogDir)
logname = currentlogDir + "\\" + logmark + ".txt"
of = open(logname, 'w')


# 改进版的logit，可以选择只记录log，不打印。而且加入了时间戳记录
def logit(text,log,i = 1):
    time = maketimestamp("time")
    log.write(time + text + "\n")
    if i == 1:
        print "<log>" + time + text + "\n"

def logit(text,of):
    time = maketimestamp("time")
    print time + text + "\n \n"
    of.write(time + text + "\n \n")

def maketimestamp(instr):
    if instr == "time":
        timestamp = time.strftime('%H:%M:%S',time.localtime(time.time()))
    elif instr == "all":
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
    else:
        print "WRONG,time calc hint is not support!"
        timestamp = "[time_WRONG]"
    return timestamp

def makeNewlog():
    rootdir = getrootDir()
    timestamp = maketimestamp("all")
    logmark = "log_" + timestamp
    logname = rootdir + "\\" + logmark + ".log"
    of = open(logname, 'w')
    return of

of = makeNewlog()
logit("haha",of)