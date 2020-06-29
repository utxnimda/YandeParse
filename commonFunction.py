import re
import time
import os
import sys
import socket
import globalValue as GVAL


g_replace = [["%20", " "],
             ["%28", "("],
             ["%29", ")"],
             ["%3A", "_"]]

def GetSaveFileName(urlPhoto, namePhoto):
    suffixFile = os.path.splitext(urlPhoto)[1]

    match = re.search(GVAL.GetNameRegex(), namePhoto)
    if(match):
        namePhoto = match.group()[:-1] + suffixFile

    return namePhoto

def Process(a, b, c):
    per = 100.0*a*b/c
    
    print("[%2.2f%%]" %(per), end="")  

    if per >= 100:
        print("[Fin]")
        
def NameReplace(name):
    name = name[33:]

    for pair in g_replace:
        name = name.replace(pair[0], pair[1])

    return name

def DelRepeat(nameList):
    for name in nameList:
        while nameList.count(name)>1:
            del nameList[nameList.index(name)]

    return nameList


def GetValueByStr(var):
    frame = sys._getframe(2)
    while(frame):
        for item in frame.f_locals.items():
            if (var is item[0]):
                    return item[1]
        frame = frame.f_back
    return None

def ChkDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def CreateFile(fullDir, filename, mode):
    path = fullDir + os.sep + filename
    
    ChkDir(fullDir)
    
    file = open(path, mode)

    print("[%s%s][%s]" % \
        (GVAL.EN2CN("Create"), GVAL.EN2CN("File"), path))

    return file

def CreateAddrFile(pat, mode):

    fullDir = GVAL.GetV("addrFullDir")
    filename = GVAL.GetFileName("addrPre", "addrExt", pat)

    return CreateFile(fullDir, filename, mode)


def CreateSuccFile(pat, mode):
    fullDir = GVAL.GetV("succLogDir")
    filename = GVAL.GetFileName("succPre", "logExt", pat)

    return CreateFile(fullDir, filename, mode)

def CreateFailFile(pat, mode):
    fullDir = GVAL.GetV("failLogDir")
    filename = GVAL.GetFileName("failPre", "logExt", pat)

    return CreateFile(fullDir, filename, mode)

def ChkOpenFile():
    download = GVAL.GetVInt("download")
    clear = GVAL.GetVInt("clear")
    addrsamefile = GVAL.GetVInt("addrsamefile")

    mode = 'a'
    if clear:
        mode = 'w'

    addrFile = None
    succFile = None
    failFile = None
    
    if not download and addrsamefile:
        addressFile = CreateAddrFile("", mode)
    
    strfTime = time.strftime("_%Y-%m-%d-%H-%M-%S")
    succFile = CreateSuccFile(strfTime, mode)
    failFile = CreateFailFile(strfTime, mode)

    return [addrFile, succFile, failFile]

def ChkOpenPoolFile(pool):
    download = GVAL.GetVInt("download")
    clear = GVAL.GetVInt("clearpool")
    addrsamefile = GVAL.GetVInt("addrsamefile")

    mode = 'a'
    if clear:
        mode = 'w'

    if not download and not addrsamefile:
        return CreateAddrFile('_' + str(pool), mode)

def ChkCloseFile(file):
    if not file == None:
        file.close()
        
def LogStart(file, key):
    if file == None:
        return 0

    
    strfTime = time.strftime("%Y.%m.%d %H:%M:%S")

    file.write("[%s%s][%s][%sID]\n" % \
        (GVAL.EN2CN("Start"), GVAL.EN2CN("Time"),
         GVAL.GetV("keyType"), GVAL.EN2CN("Img")))

                  
    file.write("[%s][%s]\n" %(strfTime, key))
    file.flush()

def LogEnd(file, key):
    if file == None:
        return 0

    
    strfTime = time.strftime("%Y.%m.%d %H:%M:%S")

    file.write("[%s][%s]\n" %(strfTime, key))
    file.write("[%s%s][%s][%sID]\n" % \
        (GVAL.EN2CN("End"), GVAL.EN2CN("Time"),
         GVAL.Get("keyType"), GVAL.EN2CN("Img")))

                  

    file.flush()


def LogInfo(file, key, action, imgID):
    if file == None:
        return 0

    strfTime = time.strftime("%Y.%m.%d %H:%M:%S")

    file.write("[%s][%s][%s%s][%s][%sID]\n" % \
        (strfTime, action,
         GVAL.GetV("keyType"), key,
         GVAL.EN2CN("ImgID"), imgID))

                  
    file.flush()
    
def PrintExt(reason):
    print("[%s][%s][%s]" % \
        (GVAL.EN2CN("Exit"),
         GVAL.EN2CN("Reason"),
         GVAL.EN2CN(reason)))


if __name__ == '__main__':
    val = {}
    a = 111
    print("[%s]" %(GetValueByStr("a")))
