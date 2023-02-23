import os
import mmap

MAP_MASK = mmap.PAGESIZE - 1

def cls(fd,mem):
    mem.close()
    os.close(fd)

def opn(addr):
    global MAP_MASK
    f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
    mem = mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE,offset=addr & ~MAP_MASK)
    return mem, f

def write_IO(address,byte):
    global MAP_MASK
    mem,f = opn(address)
    mem.seek(address & MAP_MASK)
    wrt = mem.write(byte)
    cls(f,mem)
    return wrt

def read_IO(address,length):
    global MAP_MASK
    mem,f = opn(address)
    mem.seek(address & MAP_MASK)
    vls = mem.read(length)
    cls(f,mem)
    return vls

