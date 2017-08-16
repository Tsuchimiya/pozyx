from constants import *

class Message(object):
 
    """ Defines a standard message format for client and server """
    def __init__ (self,servers_sending,msgs = None,start = False,stop = False,Filename = None,issue = None,close = False ):
        
        """ Creates a specific msg. 

            Arguments:
            servers_sending -- host sending the message (CLIENT or SERVER)
            msgs -- a byte message
        """
        
        msg = ""
        # one attribute at a time so, if there are multiple attributes like start = true + stop = true, raises an exception
        if (start and stop) or (start and not Filename is None) or (stop and not Filename is None) or ( stop and not issue is None)or (start and not issue is None) or (not Filename is None and not issue is None) or (not Filename is None and close) or (not issue is None and close) or (start and close) or (stop and close):
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
            b = bytearray()
            b.extend(map(ord, msg))
            self.msg = b
        else:
            self.msg = msgs


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
        
        


            
