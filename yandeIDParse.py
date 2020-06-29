#!\usr\bin\env python
# -*- coding: gbk -*-
import urllib
import urllib.request
import re
import time
import os
import sys
import socket

import readConfig
import commonFunction


#���ñ��ļ���
g_cfgFilename = "config.txt"
#����
g_cfg = {}
#����
g_cn = 0

#yande.re page��ַ
g_urlPre = "https://yande.re/post?page="
#yande.re tag��ַ
g_urlTag = "&tags=pool%3A"
#yande.re img��ַǰ׺
g_urlImgPre = "https://yande.re/post/show/"
#yande.re file��ַǰ׺
g_urlFilePre = "https://files.yande.re/image/"

#��·��
#window
g_rootPath = "D:\\Buf\\Yande"
#unix
#g_rootPath = "/home/data/Yande"

#�ɹ���־��
g_successLog = "SuccessLog.log"
#�ɹ���־����·��
g_successLogPath = g_rootPath + os.sep + g_successLog

#ʧ����־��
g_failLog = "FailedLog.log"
#ʧ����־����·��
g_failLogPath = g_rootPath + os.sep + g_failLog


#��ַ�ļ��ĸ�Ŀ¼
g_addressParent = "Address"
#��ַ�ļ�������Ŀ¼
g_addressFullDir = g_rootPath + os.sep + g_addressParent

#����ͼƬ��ַ���ļ�ǰ׺
g_addressPre = "address"
#����ͼƬ��ַ����·��ǰ׺
g_addressPathPre = g_addressFullDir + os.sep + g_addressPre

#�滻���ַ���
g_replaceWord = [["%20", " "],
                 ["%28", "("],
                 ["%29", ")"],
                 ["%3A", "_"]]

#����ƥ��������ַ���
g_nameRegex = r'yande.re \d* '
#ͼƬƥ��������ַ���
g_imgRegex = r'id="p\d{3,}'
#ͼƬ��ַƥ��������ַ���
g_imgAddress = r'href="https://files.yande.re/image/([\s\S]*?)"'

#Address�ļ��еķָ���
g_sep = "|"

#һ��pool���ҳ��
g_maxPoolPage = 20

g_per = 0

#ȥ��
def DelRepeat(nameList):
    for name in nameList:
        while nameList.count(name)>1:
            del nameList[nameList.index(name)]

    return nameList


#�滻�����е������ַ�
def NameReplace(name):
    name = name[33:]

    for pair in g_replaceWord:
        name = name.replace(pair[0], pair[1])

    return name


#�������
def cb(a, b, c):
    global g_per
    per = 100.0*a*b/c
    
    if per - g_per >= 5:
        print("[%2.2f%%]" %(per), end="")
        g_per = per    

    if per >= 100:
        print("[Fin]")

def ChkDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def GetSaveFileName(urlPhoto, namePhoto):
    suffixFile = os.path.splitext(urlPhoto)[1]

    match = re.search(g_nameRegex, namePhoto)
    if(match):
        namePhoto = match.group()[:-1] + suffixFile

    #print(namePhoto)
    
    return namePhoto

    
def DowloadImg(urlPhoto, namePhoto, pool):
    
    savePath = g_rootPath + os.sep + pool
    try:
        ChkDir(savePath)

        filename = GetSaveFileName(urlPhoto, namePhoto)
        fileFullname = savePath + os.sep + filename

        #print("\n" + fileFullname + "\n")
        
        urllib.request.urlretrieve(urlPhoto, fileFullname, cb)

        return 0
    except IOError as e:
        print("IOError")
        return -1
    except Exception as e:
        print("Exception")
        return -1
    except KeyboardInterrupt as e:
        print("Key Inter")
        return -1


def Dowload(urlPhoto, filename, count):
    global g_per
    
    g_per = 0
    try:
        urllib.request.urlretrieve(urlPhoto, filename, cb)

        return 0
    except IOError as e:
        print("IOERR[%d]" %(count))
        if count < 20:
            return Dowload(urlPhoto, filename, count + 1)
        return -1

def DowloadImg2(urlPhoto, namePhoto, pool):
    savePath = g_rootPath + os.sep + pool
    
    ChkDir(savePath)

    filename = GetSaveFileName(urlPhoto, namePhoto)
    fileFullname = savePath + os.sep + filename

    if os.path.exists(fileFullname):
        return 1
    

    return Dowload(urlPhoto, fileFullname, 0)
    
    
def ParseAddress(urlPhoto, namePhoto, pool, addressFile):

    try:            
        filename = GetSaveFileName(urlPhoto, namePhoto)
        
        #���ص�ַ
        addressFile.write(urlPhoto)
        addressFile.write(g_sep)
        
        #ͼƬ����pool
        addressFile.write(pool)
        addressFile.write(g_sep)
        
        #ͼƬ�ı�����
        addressFile.write(filename)
        addressFile.write("\n")
        
        addressFile.flush()

        return 0
    except IOError as e:
        print("IOError")
        return -1
    except Exception as e:
        print("Exception")
        return -1
    
def StartLog(logFile, pool):
    
    strfTime = time.strftime("%Y.%m.%d %H:%M:%S")

    logFile.write("[-----��ʼʱ��------][Pool][ImgID]\n")
    logFile.write("[%s][%s]\n" %(strfTime, pool))
    logFile.flush()

def EndLog(logFile, pool):
    strfTime = time.strftime("%Y.%m.%d %H:%M:%S")
    
    logFile.write("[%s][%s]\n" %(strfTime, pool))
    logFile.write("[-----����ʱ��------][Pool]\n\n")
    logFile.close()

def parse(successLogFile, failLogFile, pool, isDownload, addressFile):

    count = 0;
    for page in range(1, g_maxPoolPage):

        #ƴ��pool��Ӧpage��ַ
        urlPage = g_urlPre + str(page) + g_urlTag + pool 
        #��ȡhtmp��Ϣ
        htmlPage = urllib.request.urlopen(urlPage).read().decode("utf-8", "ignore")

        print("Start[%s]" %(urlPage))
        
        findIdx = re.findall(g_imgRegex, htmlPage)
        for img in findIdx:
            imgID = img[5:]
            try:
                startTime = time.time()
                count += 1
                
                print("Pool[%s] ID[%s] Page[%.3d] Num[%.3d]" %(pool, imgID, page, count));
                                                  
                urlImage = g_urlImgPre + imgID
                htmlImage = urllib.request.urlopen(urlImage).read().decode("utf-8", "ignore")
                                                     
                photosFind = DelRepeat(re.findall(g_imgAddress, htmlImage))
                if(len(photosFind) == 0):
                   continue
                
                urlPhoto = g_urlFilePre + photosFind[0]
                namePhoto = NameReplace(photosFind[0])

                action = ""
                #ȥ����
                if isDownload:
                    action = "Download"
                    ret = DowloadImg2(urlPhoto, namePhoto, pool)
                #�����أ�ֻ�ҵ�ַ
                else:
                    action = "Parse"
                    ret = ParseAddress(urlPhoto, namePhoto, pool, addressFile)
                
                endTime = time.time()
                strfTime = time.strftime("%Y.%m.%d %H:%M:%S")
                print("Pool[%s] ID[%s] Ret[%d] Cost[%.3d]sec." %(pool, imgID, ret, endTime - startTime))

                if ret == 0:
                    successLogFile.write("[%s][%.8s][%s][%s]\n" %(strfTime, action, pool, imgID))
                    successLogFile.flush()
                elif ret < 0:
                    failLogFile.write("[%s][%.8s][%s][%s]\n" %(strfTime, action, pool, imgID))
                    failLogFile.flush()
                    
            except urllib.error.URLError or socket.gaierror or NameError or ConnectionAbortedError as e:
                strfTime = time.strftime("%Y.%m.%d %H:%M:%S")
                failLogFile.write("[%s][%.8s][%s][%s]\n" %(strfTime, action, pool, imgID))
                failLogFile.flush()
                continue
            
        print("End[%s]\n" %(urlPage))
        
        if(len(findIdx) == 0):
            break;
        
def do(pool, isDownload, isClear):

    successLogFile = open(g_successLogPath, 'a')
    failLogFile = open(g_failLogPath, 'a')
    addressFile = None
    
    if not isDownload:
        ChkDir(g_addressFullDir)
        if isClear:
            addressFile = open(g_addressPathPre + '_' + str(pool) + '.txt', 'w')
        else:
            addressFile = open(g_addressPathPre + '_' + str(pool) + '.txt', 'a')

    StartLog(successLogFile, pool)
    StartLog(failLogFile, pool)

    try:
        parse(successLogFile, failLogFile, pool, isDownload, addressFile)
    except KeyboardInterrupt or AttributeError as e :
        print("Exit!")
        
    EndLog(successLogFile, pool)
    EndLog(failLogFile, pool)

    if not addressFile == None:
        addressFile.close()

def ChkCfgOne(config):
    name = commonFunction.GetName(config)
    cfgName = name[2:]
    cfgType = "Local"
    if cfgName in g_cfg:
        config = g_cfg[cfgName]
        cfgType = "Config"
        
    print("[Cfg][%s][%s %s]" %(cfgType, cfgName, config))
    
def ChkCfg():
    global g_cn
    global g_urlPre

    ChkCfgOne(g_cn)
    ChkCfgOne(g_urlPre)
    
def Main():
    global g_cfg

    Init()
    
    g_cfg = readConfig.ReadCfg(g_cfgFilename)

    ret = ChkCfg()
    
    #pool = input('����pool��')
    isDownload = True
    isClear = True

    #ChkDir(g_rootPath)

    poolList = [3940, 3943, 3944, 3945, 3947, 3948, 3949, 3950, 3951,
                3952, 3953, 3954, 3955, 3956, 3957, 3958, 3959, 3960]

    #for pool in range(3963, 3964):
        #do(str(pool), isDownload, isClear)

if __name__ == '__main__':
    Main()
