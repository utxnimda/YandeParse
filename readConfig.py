import sys
import re

def ReadCfgOne(line, cfg):
    words = re.split('\s+\|', line.strip('\n'))
    
    if len(words) > 1:
        cfg[words[0]] = words[1] 
        
def ReadCfg(cfgFilename):
    cfgFile = open(cfgFilename, "r")
    cfg = {}
    
    for line in cfgFile:
        if len(line) <= 1 or line[0] == '#':
            continue
        
        #print(len(line))
        ReadCfgOne(line, cfg)

    cfgFile.close()

    return cfg

def ReadCfgByLine(cfgFilename):
    cfgFile = open(cfgFilename, "r")
    cfg = []

    for line in cfgFile:
        if len(line) <= 1 or line[0] == '#':
            continue
        cfg.append(line.strip('\n'))
    
    cfgFile.close()

    return cfg

if __name__ == '__main__':
    filename = "config.txt"
    
    cfg = ReadCfg(filename)
    
    for one in cfg:
        print("[%s][%s]" %(one, cfg[one]))
