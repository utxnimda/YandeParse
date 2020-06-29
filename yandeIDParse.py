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


#配置表文件名
g_cfgFilename = "config.txt"
#配置
g_cfg = {}
#中文
g_cn = 0

#yande.re page地址
g_urlPre = "https://yande.re/post?page="
#yande.re tag地址
g_urlTag = "&tags=pool%3A"
#yande.re img地址前缀
g_urlImgPre = "https://yande.re/post/show/"
#yande.re file地址前缀
g_urlFilePre = "https://files.yande.re/image/"

#根路径
#window
g_rootPath = "D:\\Buf\\Yande"
#unix
#g_rootPath = "/home/data/Yande"

#成功日志名
g_successLog = "SuccessLog.log"
#成功日志绝对路径
g_successLogPath = g_rootPath + os.sep + g_successLog

#失败日志名
g_failLog = "FailedLog.log"
#失败日志绝对路径
g_failLogPath = g_rootPath + os.sep + g_failLog


#地址文件的父目录
g_addressParent = "Address"
#地址文件的完整目录
g_addressFullDir = g_rootPath + os.sep + g_addressParent

#生成图片地址的文件前缀
g_addressPre = "address"
#生成图片地址绝对路径前缀
g_addressPathPre = g_addressFullDir + os.sep + g_addressPre

#替换的字符表
g_replaceWord = [["%20", " "],
                 ["%28", "("],
                 ["%29", ")"],
                 ["%3A", "_"]]

#名字匹配的正则字符串
g_nameRegex = r'yande.re \d* '
#图片匹配的正则字符串
g_imgRegex = r'id="p\d{3,}'
#图片地址匹配的正则字符串
g_imgAddress = r'href="https://files.yande.re/image/([\s\S]*?)"'

#Address文件中的分隔符
g_sep = "|"

#一个pool最大页数
g_maxPoolPage = 20

g_per = 0

#去重
def DelRepeat(nameList):
    for name in nameList:
        while nameList.count(name)>1:
            del nameList[nameList.index(name)]

    return nameList


#替换名字中的特殊字符
def NameReplace(name):
    name = name[33:]

    for pair in g_replaceWord:
        name = name.replace(pair[0], pair[1])

    return name


#输出进度
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
        
        #下载地址
        addressFile.write(urlPhoto)
        addressFile.write(g_sep)
        
        #图片所属pool
        addressFile.write(pool)
        addressFile.write(g_sep)
        
        #图片的保存名
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

    logFile.write("[-----开始时间------][Pool][ImgID]\n")
    logFile.write("[%s][%s]\n" %(strfTime, pool))
    logFile.flush()

def EndLog(logFile, pool):
    strfTime = time.strftime("%Y.%m.%d %H:%M:%S")
    
    logFile.write("[%s][%s]\n" %(strfTime, pool))
    logFile.write("[-----结束时间------][Pool]\n\n")
    logFile.close()

def parse(successLogFile, failLogFile, pool, isDownload, addressFile):

    count = 0;
    for page in range(1, g_maxPoolPage):

        #拼好pool对应page地址
        urlPage = g_urlPre + str(page) + g_urlTag + pool 
        #获取htmp信息
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
                #去下载
                if isDownload:
                    action = "Download"
                    ret = DowloadImg2(urlPhoto, namePhoto, pool)
                #不下载，只找地址
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
    
    #pool = input('输入pool：')
    isDownload = True
    isClear = True

    #ChkDir(g_rootPath)

    poolList = [3940, 3943, 3944, 3945, 3947, 3948, 3949, 3950, 3951,
                3952, 3953, 3954, 3955, 3956, 3957, 3958, 3959, 3960]

    #for pool in range(3963, 3964):
        #do(str(pool), isDownload, isClear)

if __name__ == '__main__':
    Main()
