import multiprocessing
import sys
from stratumClientComponent import *
from GarlicoinDecoder import *
import select
def main(uri,port,user,password):
    print("start")
    talkerNet = StratumClientTalker()
    talkerWork = GarlicoinDecoder()
    #creation of the queues
    solutionQW = multiprocessing.Queue()
    workQW = multiprocessing.Queue()
    solutionQN = multiprocessing.Queue()
    workQN = multiprocessing.Queue()
    addWorkerQ = multiprocessing.Queue()
    errQ = multiprocessing.Queue()
    respQ = multiprocessing.Queue()
    #launching the method with the correct parameters
    stratumTalker = multiprocessing.Process(target=talkerNet.launchTalker,args=(uri,port,solutionQN,workQN,addWorkerQ,respQ,errQ,))
    stratumTalker.start()
    algoWorker = multiprocessing.Process(target=talkerWork.launchWorker,args=(solutionQW,workQW,))
    algoWorker.start()
    addWorkerQ.put(Worker(user,password))
   
    while True:
        ready_read,_,_ = select.select([solutionQW._reader,workQN._reader,respQ._reader,errQ._reader],[],[])
        if errQ._reader in ready_read:
            print("error in network, restarting...")
            errQ.get()
            talkerNet = StratumClientTalker()
            stratumTalker = multiprocessing.Process(target=talkerNet.launchTalker, args=(uri,port,solutionQN,workQN,addWorkerQ,respQ,errQ))
            stratumTalker.start()
            addWorkerQ.put(Worker(user,password))
        if solutionQW._reader in ready_read:
            print("SOLUTION FOUND!")
            solu = solutionQW.get()
            solutionQN.put(Solution(user,solu.job_id,solu.extranonce2,solu.ntime,solu.nonce))

        if workQN._reader in ready_read:
            blk = workQN.get()
            blk.difficulty = blk.difficulty 
            workQW.put(blk)

        if respQ._reader in ready_read:
            response = respQ.get()
            print("response - id: "+str(response.sid)+ " method: " + response.method + " invalue: " + response.invalue + " result: " + str(response.result) + " reason: " + str(response.reason))





if __name__ == "__main__":
    user = "GgCX4k45pJesNzJ6fkvqi5jzzq3YK68fJ3"
    password = "x"
    uri = "freshgarlicblocks.net"
    port = 3032

    main(uri,port,user,password)
