from ctypes import *
import struct
import hashlib
from binascii import *
from stratumStructs import *
import select

def swap_endian_word(hex_word):

    message = unhexlify(hex_word)
    return message[::-1]


def swap_endian_words(hex_words):
    byteRes = [unhexlify(hex_words)[4*i:4*i+4][::-1] for i in range(0, len(hex_words) // 4)]
    return unhexlify(''.join([byteRes[i].hex() for i in range(0,len(byteRes))]))

def sha256d(message):
    return hashlib.sha256(hashlib.sha256(message).digest()).digest()

def merkle_root_bin(blk, extranonce2_bin):
    coinbase_bin = unhexlify(blk.coinb1) + unhexlify(blk.extranonce1) + extranonce2_bin + unhexlify(blk.coinb2)
    coinbase_hash_bin = sha256d(coinbase_bin)

    merkle_root = coinbase_hash_bin
    for branch in blk.merkle_branch:
      merkle_root = sha256d(merkle_root + unhexlify(branch))
    return merkle_root

class GarlicoinDecoder:
    out_b: Array[c_char] = create_string_buffer(32) 
    difficulty = 10000
    target = (c_uint32 * 8) ()
    actualBlock = None

    def launchWorker(self,solutionQ,newWorkQ):
        libCutil = CDLL('./cutil.so',mode=RTLD_GLOBAL)
        allium = CDLL('./allium.so',mode=RTLD_GLOBAL).allium_hash
        libCutil.diff_to_targ(self.target, c_double(1))
        ver = ''
        prev = ''
        tim = ''
        bits = ''
        header = b''
        xnonce2 = 0 
        nonce = 0
        upperLimit = 2 ** 32
        targ = b''

        while True:
            ready_read, _, _= select.select([newWorkQ._reader],[],[],0)
            if newWorkQ._reader in ready_read:
                nonce = 0
                xnonce2 = 0
                self.actualBlock = newWorkQ.get()
                if self.actualBlock.difficulty/256 != self.difficulty:
                    self.difficulty = self.actualBlock.difficulty/256
                    libCutil.diff_to_targ(self.target,c_double(self.difficulty))
                    targ = b''
                    for i in range(8):
                        targ += self.target[i].to_bytes(4,'big')
                ver = swap_endian_word(self.actualBlock.version)
                prev = swap_endian_words(self.actualBlock.prevhash)
                tim = swap_endian_word(self.actualBlock.ntime)
                bits = swap_endian_word(self.actualBlock.nbits)
                header = ver + prev + merkle_root_bin(self.actualBlock,struct.pack('<I',xnonce2)) + tim + bits
            in_b: Array[c_char] = create_string_buffer(header + struct.pack('>I',nonce))
            allium(in_b,self.out_b)
            if libCutil.valid_hash(self.out_b, cast(self.target,POINTER(c_char))) == 1:
                sol = Solution(None,self.actualBlock.job_id,struct.pack('<I',xnonce2).hex(),self.actualBlock.ntime,struct.pack('<I',nonce).hex())
                solutionQ.put(sol)
            nonce = nonce + 1

