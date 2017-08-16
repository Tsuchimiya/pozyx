import socket
import message
from constants import *
import time
from threading import Thread
from localize import *
import _thread
import treat
import listen

class CTreat(treat.Treat):
    def __init__ (self,s,IHM):
        self.closing = False
        self.s = s
        self.IHM = IHM
    def start(self):
        print("[Client] start OK")

    def stop(self):
        print("[Client] stop OK")

    def filename(self,data):
        print("[Client] filename OK")

    def close(self):
        print("[Client] Closing connection")
        self.closing = True
        self.s.close()

    def issue(self,data):
        if(data.find("CONNECTION") >= 0):
            if (not self.closing):
                print("client : issue")
                self.IHM.event(CONNECT_ERROR,data)
        else:
            self.IHM.event(ISSUES,data)

class Client(object):
    """ Connects to a given server and make requests """

    def __init__ (self,IP,Port,buffer_size):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((IP,Port))


    def send_msg(self,data_to_send):
        print("[Client] sending a msg \n")
        sent = self.s.send(data_to_send.getMsg())
        if sent == 0:
            return -1
        else:
            return 1

    def getSocket(self):
        return self.s
        

if __name__ == "__main__":
    
    print("Starting client")
    C = Client(socket.gethostbyname("localhost"),5000,25)
    listener = listen.Listen(3,"Client",3,[C.getSocket(),20,CTreat(C.getSocket())])
    listener.start()
        
    m1 = message.Message(CLIENT,start = True)
    C.send_msg(m1)
    time.sleep(1)
    m = message.Message(CLIENT,Filename = "Salut")
    C.send_msg(m)
    time.sleep(1)
    C.send_msg(m)
    time.sleep(1)
    m1 = message.Message(CLIENT,stop = True)
    C.send_msg(m1)
    time.sleep(2)
    C.send_msg(m)
    time.sleep(1)
    m1 = message.Message(CLIENT,close = True)
    C.send_msg(m1)
    listener.join()
