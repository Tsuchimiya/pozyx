class Treat(object):
    def __init__(self):
        self.closing = False
        print("initialization")

    def stop(self):
        print("stop")

    def start(self):
        print("start")
        
    def filename(self,data):
        print("filename : "+data)

    def close(self):
        print("close")

    def issue(self,data):
        print("ISSUE : "+data)

    def calibrate(self,data):
        print("calibration :"+data)
