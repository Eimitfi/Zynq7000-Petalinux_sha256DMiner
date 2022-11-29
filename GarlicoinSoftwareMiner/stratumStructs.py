class Solution:
    def __init__(self,user,job_id,extranonce2,ntime,nonce):
        self.user = user
        self.job_id = job_id
        self.extranonce2 = extranonce2
        self.ntime = ntime
        self.nonce = nonce

class Worker:
    def __init__(self,user,password):
        self.user = user
        self.password = password

class ServerResponse:
    def __init__(self,sid,method,invalue,result,reason):
        self.sid = sid
        self.method = method
        self.invalue = invalue
        self.result = result
        self.reason = reason


class StratumBlockTemplate:
    def __init__(self,extranonce1,extranonce2_size, difficulty, job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime):
        self.extranonce1 = extranonce1
        self.difficulty = difficulty
        self.extranonce2_size = extranonce2_size
        self.job_id = job_id
        self.prevhash = prevhash
        self.coinb1 = coinb1
        self.coinb2 = coinb2
        self.merkle_branch = merkle_branch
        self.version = version
        self.nbits = nbits
        self.ntime = ntime
