
import subprocess

def runcmd(cmd,dir):
    p = subprocess.Popen(cmd, shell=True, cwd=dir)
    retcode = p.wait()
    return retcode


cmd_all = "ls & dir"
runcmd(cmd_all,'work')
