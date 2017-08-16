from tkinter import *
from functools import partial
import controller_PC as control
from constants import *
from time import sleep
class IHM_PC (object):

    def event(self,eventType,data):
        # updates connected status
        if (eventType == CONNECT_STATUS):
            self.connectStatus.config(text=data, fg="#5AFF33")
        if(eventType == CONNECT_ERROR):
            self.connectStatus.config(text = data,fg = "#FF3333")
        # updates  acquisition status
        if (eventType == ACQUISITION_ERROR):
            self.acquisitionStatus.config(text=data, fg="#FF3333")
        if (eventType == ACQUISITION_STATUS):
            self.acquisitionStatus.config(text=data, fg="#5AFF33")
        # updates filename status
        if(eventType == FILE_ERROR):
            self.fileStatus.config(text=data, fg="#FF3333")
        if(eventType == FILE_STATUS):
            self.fileStatus.config(text=data, fg="#5AFF33")
        if(eventType == ISSUES):
            self.issueStatus.insert(INSERT,"ISSUE: "+data+"\n")

    def start(self):
        print("start")
        self.controller.send_start()


    def stop(self):
        print("stop")
        self.controller.send_stop()

    def connect(self,lbl,IP):
        print("connecting to " + str(IP.get()))
        self.controller.connection(self,IP.get())


    def update(self):
        print("File not up to date")
        self.fileStatus.config(fg="#FF3333")

    def on_closing(self):
            print("closing connexion ...")
            self.stop()
            self.controller.close_connection()
            self.root.destroy()


    def file(self,lbl,name):
        print("filename changed to "+str(name.get()))
        if (len(name.get()) > 0):
            self.controller.send_filename(name.get())
    def __init__(self):

        self.controller = control.control()

        self.root = Tk()
        self.root.title("POZYX acquisition WiFi control")
        self.connectStatus = Label(self.root,
                             text = "CONNECTED",
                             height=2,
                             width=30,
                             fg = "#FF3333",
                             bg = "#000000")

        self.fileStatus = Label(self.root,
                             text="FILENAME UP TO DATE",
                             height=2,
                             width=30,
                             fg="#FF3333",
                             bg="#000000" )

        self.issueStatus = Text(self.root,
                                height=3,
                                width=90,
                                fg="#FF3333",
                                bg="#000000")

        self.acquisitionStatus = Label(self.root,
                           text="",
                           height=2,
                           width=30,
                           fg="#FF3333",
                           bg="#000000" )

        IPField = Label(self.root,
                        text = "IP address: ")
        filenameField = Label(self.root,
                        text = "Filename: ")
        manageField = Label(self.root,
                              text="Manage Acquisition: ")
        blank1 = Label(self.root, text = " ")
        blank = Label(self.root, text=" ")
        blank2 = Label(self.root, text=" ")

        # se connecter TODO
        IP = StringVar(self.root)
        IP.set("127.0.0.1")
        filename = StringVar(self.root)
        filename.trace("w", lambda name, index, mode, sv=filename: self.update())
        fileBox = Entry(self.root, textvariable=filename)

        connectB = Button(self.root,text = "Connect to device", command = partial(self.connect,self.connectStatus,IP))
        startB = Button(self.root,text = "Start acquisition",command = self.start)
        stopB = Button(self.root,text = "Stop acquisition",command = self.stop)
        fileB = Button(self.root, text="Confirm filename", command=partial(self.file,self.fileStatus,filename))
        IPBox = Entry(self.root,textvariable = IP)
        IPBox.config(foreground= "#000000") # TODO PUT DEFAULT VAR IN GREY



        # ROW 0
        IPField.grid(column = 0, row = 0)
        IPBox.grid(column = 1, row = 0)
        connectB.grid(column = 2, row = 0)
        self.connectStatus.grid(column = 4, row = 0)

        # ROW 1
        blank1.grid(column = 0, row = 1)

        # ROW 2
        filenameField.grid(column = 0, row = 2)
        fileBox.grid(column = 1,row = 2)
        fileB.grid(column = 2, row = 2)
        self.fileStatus.grid(column = 4, row = 2)

        # ROW 3
        blank.grid(column = 0, row = 3)

        # ROW 4
        manageField.grid(column = 0 , row = 4)
        startB.grid(column = 1,row = 4)
        stopB.grid(column = 2, row = 4)
        self.acquisitionStatus.grid(column = 4, row = 4)

        # ROW 5
        blank2.grid(column = 0, row = 5)

        # ROW 6
        self.issueStatus.grid(column = 0, row = 6, columnspan = 5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__" :
    IHM = IHM_PC()


