import time
import io
import threading
import thread
import picamera
import RPi.GPIO as gp

# initialize multi camera adapter module
# http://www.arducam.com/multi-camera-adapter-module-raspberry-pi/
print "Initializing GPIO"
gp.setwarnings(False)
gp.setmode(gp.BOARD)
   
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)
gp.setup(23, gp.OUT)
gp.setup(24, gp.OUT)

# enabling 11 and 12 represents no camera
# pin 7 becomes a don't care status
gp.output(7, False)   
gp.output(11, True)
gp.output(12, True)

# enable all other pins to disable all
# other expansion board
gp.output(15, True)
gp.output(16, True)
gp.output(21, True)
gp.output(22, True)
gp.output(23, True)
gp.output(24, True)

class Camera(object):
    thread = None
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    stopStreaming = False
    resolution = (320, 240)
    vflip = True
    hflip = True
    name = None
    mycamera = None
    
    
    def setGP(self, object):
        print "setting gpio"
        if object.cameraName == "Cam_4":
            gp.output(7, True)
            gp.output(11, True)
            gp.output(12, False)
        elif object.cameraName == "Cam_3":
            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, False)
        elif object.cameraName == "Cam_2":
            gp.output(7, True)
            gp.output(11, False)
            gp.output(12, True)
        else:
            gp.output(7, False)
            gp.output(11, False)
            gp.output(12, True)

    def setCamera(self, object):
        print "setting camera settings"
        self.name = object.cameraName
        if object.resolution == "high":
            self.mycamera.resolution = (1024, 768)
        elif object.resolution == "medium":
            self.mycamera.resolution = (800, 600)
        else:
            self.mycamera.resolution = (320, 240)
            
        self.mycamera.vflip = object.vflip
        self.mycamera.hflip = object.hflip
            
    def __init__(self, object):
        print "Instantiating camera object"
        stopStreaming = False
        self.setGP(object)
        self.mycamera = picamera.PiCamera()
        self.setCamera(object)

    def get_frame(self):
        self.last_access = time.time()
        return self.frame
    
    def startStream(self):
        print "start stream"
        if self.thread is None:
            # let camera warm up
            self.stopStreaming = False
            self.mycamera.start_preview()
            time.sleep(2)
            self.thread = CameraThread(1, self)
            self.thread.start()
            print "camera stream thread started"
    
    def stopStream(self):
        print "stopping stream"
        self.stopStreaming = True
        
        
    def readframes(self):
        
        stream = io.BytesIO()
        
        for foo in self.mycamera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
            # store frame
            stream.seek(0)
            self.frame = stream.read()
    
            # reset stream for next frame
            stream.seek(0)
            stream.truncate()
    
            # if there hasn't been any clients asking for frames in
            # the last 10 seconds stop the thread

            if time.time() - self.last_access > 5 or self.stopStreaming:
                print "killing stream"
                self.mycamera.close()
                break
            
    def takePicture(self):
        self.mycamera.startpreview()
        time.sleep(2)
        camera.capture('app/static/pics/' + self.name + time.time() + '.jpg')
            

class CameraThread(threading.Thread):
    def __init__(self, threadID, object):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.object = object
        self.name = self.object.name
        
    def run(self):
        print "Starting " + self.name
        self.object.readframes()
        self.object.thread = None
        print "End of " + self.name
        
