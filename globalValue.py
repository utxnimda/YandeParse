# -*- coding: gbk -*-
import os
import sys

import readConfig as RCFG
import commonFunction as CFUN

g_nameRegex          = r'yande.re \d* '
g_imgRegex           = r'id="p\d{3,}'
g_addrRegex          = r'href="https://files.yande.re/image/([\s\S]*?)"'

g_cfgFilename        = "cfg"

g_cfgBaseFilename    = "baseCfg"
g_cfgBaseName        = "baseCfg"
g_cfgTransName       = "transCfg"
g_cfgEN2CNName       = "en2cnCfg"


g_cfgPoolFilename    = "poolCfg"
g_cfgPoolName        = "poolCfg"
g_cfgPoolListName    = "poolListCfg"

g_cfgTagFileName     = "tagCfg"
g_cfgTagName         = "tagCfg"

g_cfgIDFileName      = "idCfg"
g_cfgIDName          = "idCfg"

g_cfgExt             = "txt"

g_cfgBaseDir         = g_cfgFilename + os.sep + g_cfgBaseFilename
g_cfgPoolDir         = g_cfgFilename + os.sep + g_cfgPoolFilename
g_cfgTagDir          = g_cfgFilename + os.sep + g_cfgTagFileName
g_cfgIDDir           = g_cfgFilename + os.sep + g_cfgIDFileName

g_cfgBasePath        = g_cfgBaseDir + os.sep + g_cfgBaseName + '.' + g_cfgExt
g_cfgTransPath       = g_cfgBaseDir + os.sep + g_cfgTransName + '.' + g_cfgExt
g_cfgEN2CNPath       = g_cfgBaseDir + os.sep + g_cfgEN2CNName + '.' + g_cfgExt

g_cfgPoolPath        = g_cfgPoolDir + os.sep + g_cfgPoolName + '.' + g_cfgExt
g_cfgPoolListPath    = g_cfgPoolDir + os.sep + g_cfgPoolListName + '.' + g_cfgExt

g_cfg                = {}
g_en2cn              = {}
g_transWords         = {}

g_GValue             = {}


g_addrFile           = None
g_succFile           = None
g_failFile           = None

def GetCV(name):
    if name in g_cfg:
        return g_cfg[name]

    return None

def GetGV(name):
    if name in g_GValue:
        return g_GValue[name]

    return None

def GetValue(name):
    value = GetCV(name)
    info = None
    if value == None:
        value = GetGV(name)
        if not value == None:
            info = "Val"
    else:
        info = "Cfg"
        
    return [value, info]

def GetV(name):
    value = GetValue(name)

    if len(value) > 0:
        return value[0]

    return None

def GetVInt(name):
    value = GetV(name)
    if value.isdigit():
        return int(value)

    return -9999


def GetAddrFile():
    return g_addrFile

def GetSuccFile():
    return g_succFile

def GetFailFile():
    return g_failFile


def SetAddrFile(file):
    global g_addrFile

    g_addrFile = file

def SetSuccFile(file):
    global g_succFile

    g_succFile = file

def SetFailFile(file):
    global g_failFile

    g_failFile = file


def GetNameRegex():
    return g_nameRegex

def GetImgRegex():
    return g_imgRegex

def GetAddrRegex():
    return g_addrRegex

def ChkValue():

    ChkValueOne("maxParsePage")
    ChkValueOne("urlPre")
    ChkValueOne("urlImgPre") 
    ChkValueOne("urlFilePre")
    ChkValueOne("urlTag")
    ChkValueOne("rootPath")

    #日志相关
    ChkValueOne("logDir")
    ChkValueOne("succPre")
    ChkValueOne("failPre")
    ChkValueOne("logExt")

    ChkValueOne("succLogDir")
    ChkValueOne("failLogDir")

    #输出地址相关
    ChkValueOne("addrDir")
    ChkValueOne("addrPre")
    ChkValueOne("addrExt")
    ChkValueOne("addrSep")

    ChkValueOne("addrFullDir")

    #保存图片文职
    ChkValueOne("imgDir")
    
    #其他
    ChkValueOne("download")
    ChkValueOne("clear")
    ChkValueOne("dlExist")
    ChkValueOne("tryTimes")
    
def ChkValueOne(name):

    value = GetValue(name)
    
    if value[1] == None:
        print("[%s%s][%s][%-15s]" % \
        (LogWord("Cfg"), \
         LogWord("Get"), \
         LogWord("Fail"), \
         name))
              
        return -1
    else:
        print("[%s%s][%s][%-15s][%s]" % \
        (LogWord(value[1]), \
         LogWord("Get"), \
         LogWord("Succ"), \
         name, value[0]))

        return 0

def CfgPoolPath():
    return g_cfgPoolPath

def CfgPoolListPath():
    return g_cfgPoolListPath


def GetFileName(name, ext, pat):
    return GetV(name) + pat + '.' + GetV(ext)

def RegEN2CN(en, cn, trans = ""):
    g_en2cn[en] = cn

    if trans == "":
        print("[Short][%-4s][EN][%-30s][CN][%s]" %(trans, en, cn))
    else:
        print("[Short][%-4s][EN][%-30s][CN][%s]" %(trans, en, cn))
        
def RegTransWord(word, en, cn):
    g_transWords[word] = en
    RegEN2CN(en, cn, word)    

def InitBase():

    BaseCfg()
    GeneBaseGlobal()

def GeneBaseGlobal():
    
    g_GValue["succLogDir"] = GetV("rootPath") + os.sep + GetV("logDir")
    g_GValue["failLogDir"] = GetV("rootPath") + os.sep + GetV("logDir")
    g_GValue["addrFullDir"] = GetV("rootPath") + os.sep +  GetV("addrDir")

    
def BaseCfg():
    AddCfg(g_cfgBasePath)
    AddEN2CNCfg(g_cfgEN2CNPath)
    AddTransCfg(g_cfgTransPath)
    
def AddCfg(cfgFilename):
    global g_cfg
    
    cfg = RCFG.ReadCfg(cfgFilename)
    g_cfg.update(cfg)

def AddEN2CNCfg(cfgFileName):
    en2cn = RCFG.ReadCfgByLine(cfgFileName)

    count = 1
    while count * 2 <= len(en2cn):
        RegEN2CN(en2cn[(count-1)*2], en2cn[count*2-1])
        count = count + 1

def AddTransCfg(cfgFileName):
    replace = RCFG.ReadCfgByLine(cfgFileName)

    count = 1
    while count * 3 <= len(replace):
        RegTransWord(replace[(count-1)*3], replace[count*3-2], replace[count*3-1])
        count = count + 1
        
 
def EN2CN(en):
    if en in g_en2cn:
        return g_en2cn[en]
    return en

def T2W(word):
    if word in g_transWords:
        return g_transWords[word]
    
    return word

def TLogWord(en):
    return LogWord(T2W(en))
    
def LogWord(en):
    if GetVInt("cn") > 0:
        return EN2CN(en)

    return en



if __name__ == '__main__':

    InitBase()
    
