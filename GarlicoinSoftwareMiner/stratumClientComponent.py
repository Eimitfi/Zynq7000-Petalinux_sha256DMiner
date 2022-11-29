import socket
from stratumStructs import *
import sys
import json
import errno
import select

#since I'm playing with sockets and select, I'm not sure this code works on windows
#the logging is shit, no time for that now

def connectToServer(uri,port):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.connect((uri,port))
        sock.setblocking(False)
    except Exception as e:
        raise Exception("can't connect, reason: " + str(e))
    return sock

#should be done with select for correctness, but for my app now is oke
def sendToServer(sock,jsonMex):
    try:
        sock.sendall(jsonMex.encode())
    except Exception as e:
        raise Exception("Error while sending " + str(jsonMex) + "reason: " + str(e))

class StratumClientTalker:
    uri = None
    port = None
    sock = None
    sid = 2 
    difficulty = 1
    extranonce1 = None
    extranonce2_size = None

    def launchTalker(self,uri,port,solutionSubmitQueue,newWorkQueue,addWorkerQueue,responseQueue,errorQueue):
        sys.stdout.flush()
        self.uri = uri
        self.port = port
        self.errorQueue = errorQueue
        self.responseQueue = responseQueue
        self.solutionSubmitQueue = solutionSubmitQueue
        self.newWorkQueue = newWorkQueue
        self.addWorkerQueue = addWorkerQueue
        self.sock = connectToServer(uri,port)
       
       #initialization communication with the server
        sendToServer(self.sock,"""{"id":1, "method": "mining.subscribe", "params": []}\n""")

        waitingResultsList = []
        response = ""
        while True:
            #not paying attention to writing IO rigth now
            ready_read, _, _= select.select([self.solutionSubmitQueue._reader, self.addWorkerQueue._reader, self.sock],[],[])

            #received something from the server
            if self.sock in ready_read:
                try:
                    repl = self.sock.recv(1).decode()
                    if repl == "":
                        self.sock.close
                        print("connection closed by peer")
                        errorQueue.put(1)
                        sys.stdout.flush()
                        sys.exit(1)
                    sys.stdout.flush()
                    response += repl
                except socket.error as e:
                    raise Exception("error while receiving, reason: " + str(e))
            #a full message from the server arrived, we better check what he has to say
                if "\n" in response:
                    message = json.loads(response)
                    print("full message received: " + response)
                    sys.stdout.flush()
                    response = ""
                    if 'method' in message:
                        if message["method"] == 'mining.notify':
                            par = message["params"]
                            blk = StratumBlockTemplate(self.extranonce1, self.extranonce2_size, self.difficulty, par[0],par[1],par[2],par[3],par[4],par[5],par[6],par[7])
                            self.newWorkQueue.put(blk)
                        elif message["method"] == "mining.set_difficulty":
                            self.difficulty = message["params"][0]

                    elif 'result' in message:
                        #only for the first response, it s needed for initialization
                        if message["id"] == 1:
                            self.extranonce1 = message["result"][1]
                            self.extranonce2_size = message["result"][2]
                            sys.stdout.flush()
                            continue
                        tmpId = message["id"]
                        result = message["result"]
                        error = message["error"]
                        #too lazy to properly check 
                        filtered = list(filter(lambda x: (x.sid == tmpId), waitingResultsList))[0]
                        waitingResultsList.remove(filtered)
                        filtered.result = result
                        filtered.reason = error
                        self.responseQueue.put(filtered)

            #submit solution method esposed to master
            if self.solutionSubmitQueue._reader in ready_read:
                solution = self.solutionSubmitQueue.get()
                submit = '{"params":["' + solution.user + '", "' + solution.job_id + '", "' + solution.extranonce2 + '", "' + solution.ntime + '", "' + solution.nonce + '"], "id":' + str(self.sid) + ', "method":"mining.submit"}\n'
                waitingResultsList.append(ServerResponse(self.sid,"solutionSubmit",solution.user + " " + solution.job_id, None,None))
                sendToServer(self.sock,submit)
                self.sid = self.sid + 1
                sys.stdout.flush()


            #addWorker method esposed to master
            if self.addWorkerQueue._reader in ready_read:
                worker = self.addWorkerQueue.get(block=False,timeout=None)
                jsonWorker = '{"params": ["' + worker.user + '", "' + worker.password + '"], "id":' + str(self.sid) + ', "method": "mining.authorize"}\n'
                waitingResultsList.append(ServerResponse(self.sid,"addWorker",worker.user, None,None))
                sendToServer(self.sock,jsonWorker)
                self.sid = self.sid + 1
                sys.stdout.flush()
                

