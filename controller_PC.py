from client import *
from IHM_PC import *

class control(object):
    def __init__ (self):
        print("Starting PC controller")
        self.C = None
    def connection(self,IHM,IP):
        print("Starting client")
        try:
            self.IHM = IHM
            self.C = Client(IP, 5000, 1024)

        except ConnectionRefusedError:
            print("Error while oppening connexion, enter IP address again")
            self.IHM.event(CONNECT_ERROR,"CONNECTION FAILED")


        self.listener = listen.Listen(3, "Client", 3, [self.C.getSocket(), 1024, CTreat(self.C.getSocket(), IHM)])
        self.listener.start()
        self.IHM.event(CONNECT_STATUS,"CONNECTED")

    def send_start(self):
        m = message.Message(CLIENT,start = True)
        if(self.C.send_msg(m) < 0):
            self.IHM.event(ACQUISITION_ERROR,"ISSUE WHILE SENDING")
        else:
            self.IHM.event(ACQUISITION_STATUS, "ACQUISITION IN PROGRESS")

    def send_stop(self):
        m = message.Message(CLIENT, stop=True)
        if (not self.C is None):
            try :
                if (self.C.send_msg(m) < 0):
                    self.IHM.event(ACQUISITION_ERROR, "ISSUE WHILE SENDING")
                else:
                    self.IHM.event(ACQUISITION_STATUS, "ACQUISITION PAUSED")
            except ConnectionResetError:
                print ("Connection failed, can't send msg")
    def send_filename(self,name):
        m = message.Message(CLIENT, Filename= name)
        if (self.C.send_msg(m) < 0):
            self.IHM.event(FILE_ERROR, "ISSUE WHILE SENDING")
        else:
            self.IHM.event(FILE_STATUS, "FILE UP TO DATE")

    def close_connection(self):
        m = message.Message(CLIENT, close= True)
        if (not self.C is None):
            try:
                if (self.C.send_msg(m) < 0):
                    raise RuntimeError ("issue while closing connexion")
            except ConnectionResetError:
                print("Connection failed, can't send msg")

