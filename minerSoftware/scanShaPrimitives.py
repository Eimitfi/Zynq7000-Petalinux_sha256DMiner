from IOprimitive import write_IO, read_IO
from addresses import *
import binascii


def stop():
    for scan in SCAN_ADDR:
        write_IO(scan,b'\x04')

def doStep():
	stop()
    for scan in SCAN_ADDR:
        write_IO(scan,b'\x01')

def start():
    for scan in SCAN_ADDR:
        write_IO(scan,b'\x81')

def readctl():
    res = []
    for scan in SCAN_ADDR:
        res.append(read_IO(scan,1))
    return res

def readHashed():
    res = []
    for scan in SCAN_ADDR:
        res.append(read_IO(scan + ACHASH,32))
    return res

def readTarget():
    res = []
    for scan in SCAN_ADDR:
        res.append(read_IO(scan + TARG,32))
    return res

def readHead():
    res = []
    for scan in SCAN_ADDR:
        res.append(read_IO(scan + HEAD,76))
    return res

def writeTarget(targets):
    i = 0
    for targ in targets:
        for x in range(len(targ)):
            write_IO(SCAN_ADDR[i] + TARG + x,targ[x].to_bytes(1,'big'))
        i += 1


def writeHead(headers):
    i = 0
    for head in headers:
        for x in range(len(head)):
            write_IO(SCAN_ADDR[i] + HEAD + x, head[x].to_bytes(1,'big'))
        i += 1
    


def readGolden():
    res = []
    for scan in SCAN_ADDR:
        res.append(int.from_bytes(read_IO(scan+GOLDEN,4),'little'))
    return res

def readActual():
    res = []
    for scan in SCAN_ADDR:
        res.append(int.from_bytes(read_IO(scan+ACTUAL,4),'little'))
    return res
