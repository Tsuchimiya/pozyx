from threading import Thread
import message
from constants import *

class Listen(Thread):

    def __init__(self, threadID, name, counter, args):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
        if len(args) == 3:
            self.co = args[0]
            self.buffer_size = args[1]
            self.treatment = args[2]
        else:
            raise RuntimeError ("[Listen] You need to pass exactly 2 arguments when instancing Listen class")
        return
    
    def treatMsg(self,msg):
        msg = message.Message(SERVER,msgs = msg)
        to_print = ""
        # if is Start : 
        ret,data = msg.isStart()
        if ret == True:
            self.treatment.start()
            to_print = "start"
            
        # if is Stop : 
        ret,data = msg.isStop()
        if ret == True:
            self.treatment.stop()
            to_print = "stop"

        # if is Filename : 
        ret,data = msg.isFilename()
        if ret == True:
            self.treatment.filename(data)
            to_print = data

        # if is Close : 
        ret,data = msg.isClose()
        if ret == True:
            self.treatment.close()
            to_print = "close"

        # if is Close : 
        ret,data = msg.isIssue()
        if ret == True:
            self.treatment.issue(data)
            to_print = data

        print("[Listen] Received :"+to_print)

    def run(self):
        while True:
            try:
                msg = self.co.recv(self.buffer_size)
                if not msg : break
                self.treatMsg(msg)
            except:
                print("listen : issue")
                self.treatment.issue("CONNECTION LOST")
                return
                break

        return 
