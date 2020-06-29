# -*- coding: gbk -*-
import urllib
import urllib.request
import re
import time
import os
import sys
import socket

import globalValue as GVAL
import yandeTagParse as YDTP
import yandePoolParse as YDPP
import yandeIDParse as YDIP
import yandeFileParse as YDFP

#配置表文件名


def Main():

    GVAL.InitBase()
    
    mode = GVAL.GetIntCfg("mode")

    if mode == 0:
        YDTP.StartParse()
    elif mode == 1:
        YDPP.StartParse()
    elif mode == 2:
        YDIP.StartParse()
    elif mode == 3:
        YDFP.StartParse()
    else:
        print("[%s%s]" %(GVAL.LogWord("Mode"),GVAL.LogWord("Error")))

if __name__ == '__main__':
    Main()
