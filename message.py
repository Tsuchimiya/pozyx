from constants import *

class Message(object):
 
    """ Defines a standard message format for client and server """
    def __init__ (self,servers_sending,msgs = None,start = False,stop = False,Filename = None,issue = None,close = False,calibrate = None ):
        
        """ Creates a specific msg. 

            Arguments:
            servers_sending -- host sending the message (CLIENT or SERVER)
            msgs -- a byte message
        """
        
        msg = ""
        # one attribute at a time so, if there are multiple attributes like start = true + stop = true, raises an exception
        if (start and stop) or (start and not Filename is None) or (stop and not Filename is None) \
                or ( stop and not issue is None)or (start and not issue is None) or (not Filename is None and not issue is None) \
                or (not Filename is None and close) or (not issue is None and close) or (start and close) or (stop and close)\
                or (not Filename is None and not calibrate is None) or (start and not calibrate is None) or (stop and not calibrate is None) \
                or (not issue is None and not calibrate is None):
            raise RuntimeError ("[Message] Error trying to send an incorrect msg : too many attributes")

        # the attribute msgs is a priority
        if msgs is None :
            if (not servers_sending):
                if start:
                    msg = msg + START
                if stop:
                    msg = msg + STOP
                if not Filename is None:
                    msg = msg + FILENAME + Filename
                if not issue is None:
                    msg = msg + ISSUE + issue
                if close:
                    msg = msg + CLOSE
                if not calibrate is None:
                    print ("MESSAGE CALIBRATION")
                    msg = msg + CALIBRATE + self.formate(calibrate)

            else:
                if start:
                    msg = msg + OK_START
                if stop:
                    msg = msg + OK_STOP
                if not Filename is None:
                    msg = msg + OK_FILENAME
                if not issue is None:
                    msg = msg + ISSUE + issue
                if close:
                    msg = msg + CLOSE
                if not calibrate is None:
                    msg = msg + OK_CALIBRATE
            b = bytearray()
            b.extend(map(ord, msg))
            self.msg = b
        else:
            self.msg = msgs

    def formate(self,anchors):
        msg = ""
        print ("MESSAGE FORMATTING")
        for i in range(len(anchors)):
            msg = msg + "A"+str(i+1) + str(anchors[i][0]) +"," + str(anchors[i][1]) + "," + str(anchors[i][2])
        print("formate = "+msg)
        return msg

    def getMsg(self):
        return self.msg

    def decode(self):
        return self.msg.decode("utf-8")

    def isStart(self):
        strMsg = self.msg.decode()
        if len(strMsg) > 0:
            if(strMsg[0] == START or strMsg[0] == OK_START):
                return [True,""]
            else:
                return [False,""]
    def isStop(self):
        strMsg = self.msg.decode()
        if len(strMsg) > 0:
            if(strMsg[0] == STOP or strMsg[0] == OK_STOP):
                return [True,""]
            else:
                return [False,""]

            
    def isClose(self):
        strMsg = self.msg.decode()
        if len(strMsg) > 0:
            if(strMsg[0] == CLOSE):
                return [True,""]
            else:
                return [False,""]

    def isIssue(self):
        strMsg = self.msg.decode()
        if len(strMsg) > 0:
            if(strMsg[0] == ISSUE ):
                return [True,strMsg[1:]]
            else:
                return [False,""]
        
    def isFilename(self):
        strMsg = self.msg.decode()
        if len(strMsg) > 0:
            if(strMsg[0] == FILENAME):
                return [True,strMsg[1:]]
            if (strMsg[0] == OK_FILENAME):
                return [True,""]
            return [False,""]
        else:
            return [False,""]

    def deformate(self,msg):
        anchors = []
        print ("[MESSAGE] DEFORMATING")
        for i in range(4):
            index= msg.find("A"+str(i+1),0)
            xindex = index+2
            yindex = msg.find(",",xindex+1)
            zindex = msg.find(",",yindex+1)
            end = msg.find("A",zindex+1)
            if end < 0:
                end = len(msg) + 1

            anchors.append([int(msg[xindex:(yindex-1)]),
                            msg[(yindex+1):(zindex-1)],
                            msg[(zindex+1):(end-1)]
                            ])

        print("deformate = "+str(anchors))
        return anchors



    def isCalibrate(self):
        strMsg = self.msg.decode()
        if len(strMsg) > 0:
            if (strMsg[0] == CALIBRATE):
                print("[MESSAGE] yeah it is an anchor calibration")
                return [True, self.deformate(strMsg[1:len(strMsg)])]
            if (strMsg[0] == OK_CALIBRATE):
                return [True, ""]
        return [False, ""]

        
        


            
