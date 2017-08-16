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

        if (eventType == CALIBRATE_ERROR):
            self.calibStatus.config(text=data, fg="#FF3333")
        if (eventType == CALIBRATE_STATUS):
            self.calibStatus.config(text=data, fg="#5AFF33")

    def start(self):
        print("start")
        self.issueStatus.delete('1.0', END)
        self.controller.send_start()



    def stop(self):
        print("stop")
        self.issueStatus.delete('1.0', END)
        self.controller.send_stop()


    def connect(self,lbl,IP):
        print("connecting to " + str(IP.get()))
        self.issueStatus.delete('1.0', END)
        self.controller.connection(self,IP.get())

    def calib(self,a1,a2,a3,a4):
        print("calibration")
        [x,y,z]= a1
        stop = False
        if (len(x.get()) <= 0 or len(y.get()) <=0 or len(z.get()) <= 0):
            self.calibStatus.config(text = "ERROR FILL ALL ANCHORS FIELDS", fg = "#FF3333")
            stop = True
        a11 = [x.get(),y.get(),z.get()]

        [x, y, z] = a2
        if (len(x.get()) <= 0 or len(y.get()) <= 0 or len(z.get()) <= 0):
            self.calibStatus.config(text="ERROR FILL ALL ANCHORS FIELDS", fg="#FF3333")
            stop = True
        a22 = [x.get(), y.get(), z.get()]

        [x, y, z] = a3
        if (len(x.get()) <= 0 or len(y.get()) <= 0 or len(z.get()) <= 0):
            self.calibStatus.config(text="ERROR FILL ALL ANCHORS FIELDS", fg="#FF3333")
            stop = True
        a33 = [x.get(), y.get(), z.get()]

        [x, y, z] = a4
        if (len(x.get()) <= 0 or len(y.get()) <= 0 or len(z.get()) <= 0):
            self.calibStatus.config(text="ERROR FILL ALL ANCHORS FIELDS", fg="#FF3333")
            stop = True
        a44 = [x.get(), y.get(), z.get()]

        if (not stop):
            self.controller.send_calib([a11,a22,a33,a44])

            print ("[IHM] : calib " + str([a11,a22,a33,a44]))

    def update(self):
        print("File not up to date")
        self.issueStatus.delete('1.0', END)
        self.fileStatus.config(fg="#FF3333")

    def on_closing(self):
            print("closing connexion ...")
            self.issueStatus.delete('1.0', END)
            self.stop()
            self.controller.close_connection()
            self.root.destroy()


    def file(self,lbl,name):
        self.issueStatus.delete('1.0', END)
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

        self.calibStatus = Label(self.root,
                                       text="WAITING FOR CALIBRATION",
                                       height=2,

                                       width=30,
                                       fg="#FF3333",
                                       bg="#000000")

        IPField = Label(self.root,
                        text = "IP address: ")
        filenameField = Label(self.root,
                        text = "Filename: ")

        calibdescB = Label(self.root,
                           text="Calibration Fields (just calibrate once after connecting)",
                           font= "bold",
                           relief = RIDGE,
                           width = 90,
                           borderwidth = 1)

        manageField = Label(self.root,
                              text="Manage Acquisition: ")
        anch1Field = Label(self.root,
                        text="Anchor x6121: ")
        anch2Field = Label(self.root,
                        text="Anchor x6115: ")
        anch3Field = Label(self.root,
                           text="Anchor x6157: ")
        anch4Field = Label(self.root,
                           text="Anchor x6109: ")

        xField = Label(self.root,
                           text="X (mm) = ")
        yField = Label(self.root,
                       text="Y (mm) = ")
        zField = Label(self.root,
                       text="Z (mm) = ")

        blank1 = Label(self.root, text = " ")
        blank = Label(self.root, text=" ")
        blank2 = Label(self.root, text=" ")
        blank3 = Label(self.root, text=" ")

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

        x1 = StringVar(self.root)
        x1Box = Entry(self.root, textvariable=x1, width = 6)
        x2 = StringVar(self.root)
        x2Box = Entry(self.root, textvariable=x2, width = 6)
        x3 = StringVar(self.root)
        x3Box = Entry(self.root, textvariable=x3, width = 6)
        x4 = StringVar(self.root)
        x4Box = Entry(self.root, textvariable=x4, width = 6)

        y1 = StringVar(self.root)
        y1Box = Entry(self.root, textvariable=y1, width = 6)
        y2 = StringVar(self.root)
        y2Box = Entry(self.root, textvariable=y2, width = 6)
        y3 = StringVar(self.root)
        y3Box = Entry(self.root, textvariable=y3, width = 6)
        y4 = StringVar(self.root)
        y4Box = Entry(self.root, textvariable=y4, width = 6)

        z1 = StringVar(self.root)
        z1Box = Entry(self.root, textvariable=z1, width = 6)
        z2 = StringVar(self.root)
        z2Box = Entry(self.root, textvariable=z2, width = 6)
        z3 = StringVar(self.root)
        z3Box = Entry(self.root, textvariable=z3, width = 6)
        z4 = StringVar(self.root)
        z4Box = Entry(self.root, textvariable=z4, width = 6)

        calibB = Button(self.root, text="Calibrate",
                        command=partial(self.calib, [x1, y1, z1], [x2, y2, z2], [x3, y3, z3], [x4, y4, z4]))


        # ROW 0
        IPField.grid(column = 3, row = 0)
        IPBox.grid(column = 4, row = 0)
        connectB.grid(column = 5, row = 0)
        self.connectStatus.grid(column = 6, row = 0)

        # ROW 1
        blank1.grid(column = 0, row = 1)

        # ROW 2
        filenameField.grid(column = 3, row = 2)
        fileBox.grid(column = 4,row = 2)
        fileB.grid(column = 5, row = 2)
        self.fileStatus.grid(column = 6, row = 2)

        # ROW 3
        blank.grid(column =0, row = 3)

        # ROW 4
        calibdescB.grid(column = 0,columnspan = 7, row = 4)

        # ROW 5
        calibB.grid(column = 5, row = 4, rowspan = 5)
        self.calibStatus.grid(column = 6, row = 5, rowspan = 4)
        anch1Field.grid(column = 1 , row = 5)
        anch2Field.grid(column = 2, row=5)
        anch3Field.grid(column = 3, row=5)
        anch4Field.grid(column = 4, row=5)

        # ROW 6
        xField.grid(column = 0, row = 6)
        x1Box.grid(column = 1, row = 6)
        x2Box.grid(column=2, row=6)
        x3Box.grid(column=3, row=6)
        x4Box.grid(column=4, row=6)


        # ROW 7
        yField.grid(column=0, row=7)
        y1Box.grid(column=1, row=7)
        y2Box.grid(column=2, row=7)
        y3Box.grid(column=3, row=7)
        y4Box.grid(column=4, row=7)

        # ROW 8
        zField.grid(column=0, row=8)
        z1Box.grid(column=1, row=8)
        z2Box.grid(column=2, row=8)
        z3Box.grid(column=3, row=8)
        z4Box.grid(column=4, row=8)

        # ROW 9
        blank3.grid(column=0, row=9)

        # ROW 10
        manageField.grid(column=3, row=10)
        startB.grid(column=4, row=10)
        stopB.grid(column=5, row=10)
        self.acquisitionStatus.grid(column=6, row=10)

        # ROW 11
        blank2.grid(column=0, row=11)

        # ROW 12
        self.issueStatus.grid(column = 0, row = 12, columnspan = 7)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__" :
    IHM = IHM_PC()


