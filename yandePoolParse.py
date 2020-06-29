#!\usr\bin\env python
# -*- coding: gbk -*-
import time
import os
import sys

import globalValue as GVAL
import commonFunction as CFUN
import readConfig as RCFG
import parse as PARSE

global g_addrFile
global g_succFile
global g_failFile

#获取pool list类型
g_poolList        = []
g_startPool       = 0
g_endPool         = 1

def ParsePage(pool):
    maxPoolPage = GVAL.GetVInt("maxParsePage")
    
    for page in range(1, maxPoolPage):
        
        urlPage = GVAL.GetV("urlPre") + str(page) + GVAL.GetV("urlTag") + GVAL.GetV("urlPoolTag") +str(pool)
        #print(urlPage)
        ret = PARSE.ParsePageOne(urlPage, pool, page)

        if ret != 0:
            break;
     
def DoParse():
    global g_addrFile
    global g_succFile
    global g_failFile
    
    poolType = GVAL.GetVInt("poolType")

    file = CFUN.ChkOpenFile()
    GVAL.SetAddrFile(file[0])
    GVAL.SetSuccFile(file[1])
    GVAL.SetFailFile(file[2])
                     
    if poolType == 0 or poolType == 2:
        for pool in g_poolList:
            ParseOne(pool)
    elif poolType == 1 or poolType == 3: 
        for pool in range(g_startPool, g_endPool + 1):
            ParseOne(pool)
    else:
        PrintErrType()
        return -1

    return 0

    CFUN.ChkCloseFile(GVAL.GetSuccFile())
    CFUN.ChkCloseFile(GVAL.GetFailFile())

def ParseOne(pool):
    
    if not GVAL.GetVInt("addrsamefile"):
        GVAL.SetAddrFile(CFUN.ChkOpenPoolFile(pool))
            
    CFUN.LogStart(GVAL.GetSuccFile(), pool)
    CFUN.LogStart(GVAL.GetFailFile(), pool)

    ParsePage(pool)

    CFUN.LogEnd(GVAL.GetSuccFile(), pool)
    CFUN.LogEnd(GVAL.GetFailFile(), pool)

    if not GVAL.GetVInt("addrsamefile"):
        CFUN.ChkCloseFile(GVAL.GetAddrFile())


def PrintPoolList():
    print("[%s:" %(GVAL.TLogWord("PPID")))
    print("[", end="")
    count = 0
    for pool in g_poolList:
        if count == 0:
            print("%d" %(pool), end="")
        else:
            print(" %d" %(pool), end="")
        count = count + 1
    print("]")

def PrintPoolRange():
    print("[%s:" %(GVAL.TLogWord("PPR")))
    print("[%d %d]" %(g_startPool, g_endPool))


def PrintErrType():
    print("[%s%s][%d]" %(GVAL.EN2CN("Error"), (GVAL.EN2CN("Type")), GVAL.GetVInt("poolType")))
    
def DoPoolIDInput(hint, hintFail):
    while True:
        pool = input("[%s: " %(GVAL.TLogWord(hint)))
        if pool.isdigit():
            return int(pool)
        else:
            return DoPoolIDInput(hintFail, hintFail)
    
def GetPoolList():
    global g_poolList
    
    poolType = GVAL.GetVInt("poolType")
    
    
    if poolType == 0:
        while True:
            pool = DoPoolIDInput("PIP", "PIVI")
            if int(pool) > 0:
                g_poolList.append(int(pool))
            else:
                break

        g_poolList = list(set(g_poolList))
        PrintPoolList()
        
    elif poolType == 1:
        g_startPool = DoPoolIDInput("PISP", "PIVI")
        g_endPool = DoPoolIDInput("PIEP", "PIVI")

        PrintPoolRange()
        
    elif poolType == 2:
        cfgPoolList = RCFG.ReadCfgByLine(GVAL.CfgPoolListPath())
        for pool in cfgPoolList:
            if pool.isdigit():
                g_poolList.append(int(pool))

        g_poolList = list(set(g_poolList))
        PrintPoolList()
        
    elif poolType == 3:
        g_startPool = GVAL.GetV("startPool")
        g_startPool = GVAL.GetV("endPool")
        
        PrintPoolRange()
    else:
        PrintErrType()
        return -1

    return 0    


def CheckVal():
    GVAL.ChkValue()
    
    GVAL.ChkValueOne("urlPoolTag")
    GVAL.ChkValueOne("poolType")
    GVAL.ChkValueOne("startPool")
    GVAL.ChkValueOne("endPool")
    GVAL.ChkValueOne("keyType")
    
def StartParse():
    
    GVAL.AddCfg(GVAL.CfgPoolPath())
    CheckVal()
    
    ret = GetPoolList()

    if ret == 0:
        try:
            DoParse()
        except KeyboardInterrupt as e:
            CFUN.PrintExt("KeyboardInterrupt")
            CFUN.ChkCloseFile(GVAL.GetAddrFile())
            CFUN.ChkCloseFile(GVAL.GetSuccFile())
            CFUN.ChkCloseFile(GVAL.GetFailFile())
            return
        except Exception as e:
            CFUN.PrintExt("Exception")
            CFUN.ChkCloseFile(GVAL.GetAddrFile())
            CFUN.ChkCloseFile(GVAL.GetSuccFile())
            CFUN.ChkCloseFile(GVAL.GetFailFile())
            return
        
    CFUN.PrintExt("Finish")
                
if __name__ == '__main__':
    GVAL.InitBase()

    StartParse()
