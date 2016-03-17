import time
import io
import threading
import picamera
import RPi.GPIO as gp

# initialize multi camera adapter module
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
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    

    def initialize(self):
        if Camera.thread is None:
            Camera.stop_request = False
            
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera 1 setup
            gp.output(7, True)
            gp.output(11, False)
            gp.output(12, True)
            camera.resolution = self.resolution
            camera.hflip = self.hflip
            camera.vflip = self.vflip

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
                
                ## check to see if a request to stop was issued
                if Camera.stop_request:
                    break

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break

            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, True)
            cls.thread = None

    def stop_streaming(self):
        Camera.stop_request = True

