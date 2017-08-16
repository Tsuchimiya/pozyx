import socket
from constants import *
import message
import listen
import treat
import threading
import _thread
from time import sleep
import message
import ready_to_localize
import os

def prout(start,changeFile,fileSem):
    for i in range(50):
        start.wait()
        if(not changeFile.isSet()):
            fileSem.acquire()
            file = open("filename.txt","r")
            name = file.read()
            file.close()
            print("Filename changed "+name+"\n")
            fileSem.release()
            changeFile.set()
        print("thread \n")
        sleep(1)
    return
    
class STreat(treat.Treat):
    def __init__ (self,serveur):
        self.serveur = serveur
        self.flagStart = threading.Event()
        self.flagStart.clear()
        self.flagFile = threading.Event()
        self.flagFile.clear()
        self.sem = threading.Semaphore(value = 0)
        self.prefix = ""
        file = open("/tmp/filename.txt","w",1) # todo on odroid
        file.write("default")
        file.close()
        self.thread = _thread.start_new_thread( ready_to_localize.main_localize, (self.flagStart,self.flagFile,self.sem,self) )
        self.sem.release()


    # changing filename of the thread POZYX
    def filename(self,name):

        print("changing filename of pozyx: name "+name)
        self.sem.acquire()
        file = open("/tmp/filename.txt","w",1) # todo on odroid
        file.write(name)
        file.close()
        self.flagFile.clear()
        self.sem.release()

            #m = message.Message(SERVER,Filename = "Ok")
            #self.serveur.send_msg(m)

    # starting the thread POZYX
    def start(self):
        self.flagStart.set()

        #m = message.Message(SERVER,start = True)
        #self.serveur.send_msg(m)
        
    # stopping the thread POZYX
    def stop(self):
        self.flagStart.clear()
        self.send_stop()

    def close(self):
        self.flagStart.clear()
        #m = message.Message(SERVER,close = True)
        #self.serveur.send_msg(m)
        self.serveur.close()

    def send_start(self):
        m = message.Message(SERVER, start=True)
        self.serveur.send_msg(m)

    def send_stop(self):
        m = message.Message(SERVER, stop=True)
        self.serveur.send_msg(m)

    def send_close(self):
        m = message.Message(SERVER, close=True)
        self.serveur.send_msg(m)

    def send_filename(self):
        m = message.Message(SERVER, Filename="Ok")
        self.serveur.send_msg(m)

    def send_issue(self,data):
        m = message.Message(SERVER, issue=data)
        self.serveur.send_msg(m)

class Serveur(object):
    """ Receives requests from a distant host and responds to them """

    def __init__(self,IP,Port,buffer_size):
       
        """ implements a serveur binded on the given IP adress and port """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((IP,Port))
        self.s.listen(1)

        # waiting and accepting a client connexion
        self.co,self.addr = self.s.accept()
        print("[Server] Connected with address: "+str(self.addr))

        self.treat = STreat(self)
        self.listen = listen.Listen(1, "Listen_Serveur",1,args = [self.co,buffer_size,self.treat] )
        self.listen.start()
        self.listen.join()
        
    def send_msg(self,data_to_send):
        print("[Server] sending data")
        self.co.send(data_to_send.getMsg())

    def close(self):
        print("[Server] Closing connection")
        self.s.close()
        
if __name__ == "__main__":
    print("Starting server")
    S = Serveur(socket.gethostbyname("localhost"),5000,1024)
    
