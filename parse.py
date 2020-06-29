import urllib
import urllib.request
import re
import time
import os

import globalValue as GVAL
import commonFunction as CFUN

#替换名字中的特殊字符

def ParseAddress(urlPhoto, namePhoto, key):


    addrFile = GVAL.GetAddrFile()
    if addrFile == None:
        return -1

    try:
        filename = CFUN.GetSaveFileName(urlPhoto, namePhoto)
        
        #下载地址
        addrFile.write(urlPhoto)
        addrFile.write(GVAL.GetV("addrSep"))
        
        #图片所属pool
        addrFile.write(str(key))
        addrFile.write(GVAL.GetV("addrSep"))
        
        #图片的保存名
        addrFile.write(filename)
        addrFile.write("\n")
        
        addrFile.flush()

        return 0
    except IOError as e:
        print("[IOError]")
        return -1
    except Exception as e:
        print("[Exception]")
        return -1

    
def Dowload(urlPhoto, filename, count):
    try:
        urllib.request.urlretrieve(urlPhoto, filename)

        return 0
    except IOError as e:
        print("IOERR[%d]" %(count))
        if count < GVAL.GetV("tryTimes"):
            return Dowload(urlPhoto, filename, count + 1)
        return -1

def DowloadImg(urlPhoto, namePhoto, key):

    savePath = GVAL.GetV("rootPath") + os.sep + GVAL.GetV("imgDir") + os.sep + str(GVAL.GetV("keyType")) + os.sep + str(key) 
    #print(savePath)
    
    CFUN.ChkDir(savePath)

    filename = CFUN.GetSaveFileName(urlPhoto, namePhoto)
    fileFullname = savePath + os.sep + filename

    if not GVAL.GetV("dlExist") and os.path.exists(fileFullname):
        return 1
    
    return Dowload(urlPhoto, fileFullname, 0)
    
def ParsePageOne(urlPage, key, page):
    download = GVAL.GetVInt("download")
        
    #获取html信息
    htmlPage = urllib.request.urlopen(urlPage).read().decode("utf-8", "ignore")

    print("[%s%s][%s]" % (GVAL.EN2CN("Start"), GVAL.EN2CN("Url"), urlPage))

    count = 0

    findIdx = re.findall(GVAL.GetImgRegex(), htmlPage)
    #print(findIdx)
    for img in findIdx:
        imgID = img[5:]
        try:
            startTime = time.time()
            count += 1

            action = ""
            if download:
                action = GVAL.EN2CN("Download")
            else:
                action = GVAL.EN2CN("GetAddress")
                
            print("[%s][%s %s][%s %s][%s %.3d][%s %.3d][%s]" % \
                   (action, GVAL.EN2CN(GVAL.GetV("keyType")), key, 
                    GVAL.EN2CN("ImgID"), imgID,
                    GVAL.EN2CN("Page"),  page,
                    GVAL.EN2CN("Count"), count,
                    GVAL.EN2CN("Start")))
                                              
            urlImage = GVAL.GetV("urlImgPre") + imgID
            htmlImage = urllib.request.urlopen(urlImage).read().decode("utf-8", "ignore")
            
            photosFind = CFUN.DelRepeat(re.findall(GVAL.GetAddrRegex(), htmlImage))
            if(len(photosFind) == 0):
               continue

            urlPhoto = GVAL.GetV("urlFilePre") + photosFind[0]
            namePhoto = CFUN.NameReplace(photosFind[0])
            
            if download:
                ret = DowloadImg(urlPhoto, namePhoto, key)
            else:
                ret = ParseAddress(urlPhoto, namePhoto, key)
            
            endTime = time.time()
            print("[%s][%s %s][%s %s][%s %.3d][%s %.3d][%s %s][%s %3d][%s]" % \
                   (action, GVAL.EN2CN(GVAL.GetV("keyType")), key,
                    GVAL.EN2CN("ImgID"), imgID,
                    GVAL.EN2CN("Page"),  page,
                    GVAL.EN2CN("Count"), count,
                    GVAL.EN2CN("Ret"), ret,
                    GVAL.EN2CN("Cost"), endTime - startTime,
                    GVAL.EN2CN("Sec")))

            if ret == 0:
                CFUN.LogInfo(GVAL.GetSuccFile(), key, action, imgID)
            elif ret < 0:
                CFUN.LogInfo(GVAL.GetFailFile(), key, action, imgID)
                
        except urllib.error.URLError or socket.gaierror or NameError or ConnectionAbortedError as e:
            LogInfo(GVAL.GetFailFile(), pool, action, imgID)
            continue
        
    print("[%s%s][%s][%s][%s %d]" % (GVAL.EN2CN("End"), GVAL.EN2CN("Url"), urlPage, GVAL.EN2CN("Success"), count))
    
    if(len(findIdx) == 0):
        return -1
        
