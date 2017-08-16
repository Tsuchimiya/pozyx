#!/usr/bin/env python
## https://github.com/pozyxLabs/Pozyx-Python-library/archive/master.zip
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python

This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as you move your device around!
"""
from time import sleep

from pypozyx import *
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import os
import time

class ReadyToLocalize(object):
    """Continuously calls the Pozyx positioning function and prints its position."""

    def __init__(self, pozyx, osc_udp_client, anchors, filename, treat,
                 algorithm=POZYX_POS_ALG_UWB_ONLY, dimension=POZYX_3D, height=1000, remote_id=None):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client
        self.treat = treat
        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.remote_id = remote_id
        self.prefix = ""

        # if we are not into pozyx directory going into it 
        if(os.getcwd().find("POZYX",0) < 0):
            self.prefix = "/home/odroid/POZYX/"
        if not os.path.isdir(self.prefix+'output'):
            os.mkdir(self.prefix+'output')

        # setting a file number if there is already a file in the directory
        path = self.prefix + "output/"
        if (os.listdir(path).__contains__(filename)):
            return None
        path = path + filename + ".txt"
        self.file = open(path,"w",1)

    def updateFilename (self,filename):

        if (os.listdir(self.prefix+'output/').__contains__(filename)):
            return -2
        else :
            self.file.close()
            self.file = open(self.prefix+'output/'+filename+".txt","w",1)
            return 0

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX POSITIONING V1.1 -------------")
        print("NOTES: ")
        print("- No parameters required.")
        print()
        print("- System will auto start configuration")
        print()
        print("- System will auto start positioning")
        print("------------POZYX POSITIONING V1.1 --------------")
        print()
        print("START Ranging: ")
        self.pozyx.clearDevices(self.remote_id)
        self.setAnchorsManual()
        self.printPublishConfigurationResult()

    def loop(self):
        """Performs positioning and displays/exports the results."""
        position = Coordinates()
        status = self.pozyx.doPositioning(
            position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
        if status == POZYX_SUCCESS:
            self.printPublishPosition(position)
            self.store_position(position)
        else:
            self.printPublishErrorCode("positioning")

    def store_position(self,position):
        """ Stores a position log into a file """
        if not (self.file is None):
            seconds = int(time.strftime("%S"))
            minutes = int (time.strftime("%M")) * 60
            hours = int(time.strftime("%H")) * 60 * 60
            line = "T="+str(seconds+minutes+hours)+"\t X="+str(position.x)+"\t Y="+str(position.y)+"\t Z="+str(position.z)
            self.file.write(line+"\n")

    def printPublishPosition(self, position):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        print("POS ID {}, x(mm): {pos.x} y(mm): {pos.y} z(mm): {pos.z}".format(
            "0x%0.4x" % network_id, pos=position))
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(position.x), int(position.y), int(position.z)])

    def printPublishErrorCode(self, operation):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        network_id = self.remote_id
        if network_id is None:
            self.pozyx.getErrorCode(error_code)
            issue = "ERROR" + str(operation) +", error code " + str(error_code)
            self.treat.send_issue(issue)

            print("ERROR %s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, error_code[0]])
            return
        status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if status == POZYX_SUCCESS:
            print("ERROR %s on ID %s, error code %s" %
                  (operation, "0x%0.4x" % network_id, str(error_code)))
            issue = "ERROR" + str(operation)+" on ID "+str(network_id) +", error code "+str(error_code)
            self.treat.send_issue(issue)
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error", [operation, network_id, error_code[0]])
        else:
            self.pozyx.getErrorCode(error_code)
            print("ERROR %s, couldn't retrieve remote error code, local error code %s" %
                  (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, -1])
            # should only happen when not being able to communicate with a remote Pozyx.

    def setAnchorsManual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        status = self.pozyx.clearDevices(self.remote_id)
        for anchor in self.anchors:
            status &= self.pozyx.addDevice(anchor, self.remote_id)
        if len(self.anchors) > 4:
            status &= self.pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, len(anchors))
        return status

    def printPublishConfigurationResult(self):
        """Prints and potentially publishes the anchor configuration result in a human-readable way."""
        list_size = SingleRegister()

        status = self.pozyx.getDeviceListSize(list_size, self.remote_id)
        print("List size: {0}".format(list_size[0]))
        if list_size[0] != len(self.anchors):
            self.printPublishErrorCode("configuration")
            return
        device_list = DeviceList(list_size=list_size[0])
        status = self.pozyx.getDeviceIds(device_list, self.remote_id)
        print("Calibration result:")
        print("Anchors found: {0}".format(list_size[0]))
        print("Anchor IDs: ", device_list)

        for i in range(list_size[0]):
            anchor_coordinates = Coordinates()
            status = self.pozyx.getDeviceCoordinates(
                device_list[i], anchor_coordinates, self.remote_id)
            print("ANCHOR,0x%0.4x, %s" % (device_list[i], str(anchor_coordinates)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [device_list[i], int(anchor_coordinates.x), int(anchor_coordinates.y), int(anchor_coordinates.z)])
                sleep(0.025)

    def printPublishAnchorConfiguration(self):
        """Prints and potentially publishes the anchor configuration"""
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.coordinates)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, int(anchor.coordinates.x), int(anchor.coordinates.y), int(anchor.coordinates.z)])
                sleep(0.025)

def main_localize(start,changeFile,calib,fileSem,calibSem,treat):
    serial_port = None
    try :
        serial_port = get_serial_ports()[0].device
    except:
        treat.send_issue("Problem while connecting to POZYX")
    print("serial" + serial_port)
    remote_id = 0x6069  # remote device network ID
    remote = False  # whether to use a remote device
    if not remote:
        remote_id = None

    use_processing = True  # enable to send position data through OSC
    ip = "127.0.0.1"  # IP for the OSC UDP
    network_port = 8888  # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)
        # necessary data for calibration, change the IDs and coordinates yourself
    print ("[LOCALIZE] waiting for calibration")
    calib.wait()
    anchors = []
    names = [0x6121,0x6115,0x6157,0x6109]
    calibSem.acquire()
    file = open("/tmp/anchors.txt","r")
    for i in range(4):
        line = file.readline()
        print("[LOCALIZE] line = "+line+" names = "+str(names[i]))
        indx = line.find(",",0)
        indy = line.find(",",indx + 1 )
        anchors.append(DeviceCoordinates(names[i],
                                         Coordinates(int(line[0:(indx)]),
                                                     int(line[(indx +1):(indy)]),
                                                     int(line[(indy + 1):(len(line))])
                                                     ) ) )
    print ("[LOCALIZE] Calibration succeeded")
    treat.send_calibrate()
    file.close()
    calibSem.release()
    #anchors = [DeviceCoordinates(0x6121, 1, Coordinates(2750, 30, 1780)),
      #             DeviceCoordinates(0x6115, 1, Coordinates(3500, 4750, 1460)),
       #            DeviceCoordinates(0x6157, 1, Coordinates(167, 8250, 1950)),
        #           DeviceCoordinates(0x6109, 1, Coordinates(30, 30, 930))]

    algorithm = POZYX_POS_ALG_TRACKING  # positioning algorithm to use
    dimension = POZYX_3D  # positioning dimension
    height = 1000  # height of device, required in 2.5D positioning
    pozyx = None
    try:
        pozyx = PozyxSerial(serial_port)
    except:
        treat.send_issue("Problem while connecting to POZYX")


    r = None
    while True:
        start.wait()
        if(not changeFile.isSet()):
            fileSem.acquire()
            file = open("/tmp/filename.txt","r")
            name = file.read()
            print("LOCALIZE: name"+name)

            file.close()
            fileSem.release()
            if not r is None:
                if (r.updateFilename(name) < 0):
                    treat.send_issue("File exists already")
                else:
                    treat.send_filename()
            else:
                r = ReadyToLocalize(pozyx, osc_udp_client, anchors, name,treat, algorithm, dimension, height, remote_id)
                treat.send_filename()

            if (r is None):
                treat.send_issue("File exists already")
            r.setup()
            print("Filename changed "+name+"\n")

            changeFile.set()
        try:
            r.loop()
        except:
            treat.send_issue("Issue while positionning... (check anchors)")
    return
if __name__ == "__main__":
    sleep(5)
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[0].device
    print("serial"+serial_port)
    remote_id = 0x6069               # remote device network ID
    remote = False                   # whether to use a remote device
    if not remote:
        remote_id = None

    use_processing = True             # enable to send position data through OSC
    ip = "127.0.0.1"                   # IP for the OSC UDP
    network_port = 8888                # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)
    # necessary data for calibration, change the IDs and coordinates yourself
    anchors = [DeviceCoordinates(0x6121, 1, Coordinates(2750, 30, 1780)),
               DeviceCoordinates(0x6115, 1, Coordinates(3500, 4750, 1460)),
               DeviceCoordinates(0x6157, 1, Coordinates(167, 8250, 1950)),
               DeviceCoordinates(0x6109, 1, Coordinates(30, 30, 930))]

    algorithm = POZYX_POS_ALG_TRACKING  # positioning algorithm to use
    dimension = POZYX_3D               # positioning dimension
    height = 1000                      # height of device, required in 2.5D positioning
    sleep(50)
    pozyx = PozyxSerial(serial_port)
    r = ReadyToLocalize(pozyx, osc_udp_client, anchors, algorithm, dimension, height, remote_id,file_numbers = 1)
    r.setup()
    while True:
        r.loop()


##
# curl -O https://bootstrap.pypa.io/get-pip.py
# sudo python3.2 get-pip.py
