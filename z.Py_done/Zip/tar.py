import tarfile
import os
def untar(fpath,fname, outdir):
    n = fpath +"\\"+fname
    print ('unzip the tar file %s' % n)
    tar = tarfile.open(n)
    tar.extractall(path = outdir)
    tar.close()

def eraseFolder(dir):
    import shutil
    shutil.rmtree(dir,True)

if __name__ == "__main__":
    gzPath = "D:\waka"
    out = "C:\Temp_a"
    gzname = "BTS_D_RF.tar.gz"
    eraseFolder(out)
    untar(gzPath,gzname,out)
    #now upgrade folder will lie in out\BTS_D_RF
