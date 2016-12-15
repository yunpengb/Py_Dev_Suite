import os
import shutil

def copytypeFilesReturnName(sourceDir,targetDir,type):
    typefiles = []
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,files)
        targetFile = os.path.join(targetDir,files)
        if os.path.isfile(sourceFile) and sourceFile.find(type)>0:
            typefiles.append(files)
            shutil.copy(sourceFile,targetFile)
        typename = " ".join(str(i) for i in typefiles)
    return typename

def getLarName(lardir):
    i = os.listdir(lardir)
    name = findstr(i,'.LAR')
    j = name[0]+" "+name[1]
    return j

def getdirlist(dir):
    i = os.listdir(dir)
    return i

def findstr(rlist, onestr):
    found = []
    for element in rlist:
        if onestr in element:
            found.append(element)
    return found

def fileloadRP1(exedir,larStr,unitip):
    command = "FileLoaderRp1.exe -i " + unitip + ' -b "name" -l ' + larStr + ' -m ALL -v 2'
    cmd1 = 'cd '+exedir
    os.system(cmd1)

if __name__ == "__main__":
    m = getdirlist('C:\Temp_a')
    type = '.LAR'
    updir = m[0] # get the upgrade folder name
    sourceDir = 'C:\\Temp_a\\' + updir +"\C_Element\SE_RFM\SS_REL3\Target"
    targetDir = 'C:\\Temp_a\\'+ updir + "\C_Element\SE_RFM\SS_REL3\RnD"
    lar = copytypeFilesReturnName(sourceDir,targetDir,type)
    print lar
    print "copy lar file done!"

