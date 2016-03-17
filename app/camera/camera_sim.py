from time import time

class Camera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    

    def __init__(self, resolution, vflip, hflip):
        self.resolution = resolution
        self.vflip = vflip
        self.hflip = hflip
        print self.resolution
        print self.vflip
        print self.hflip
        self.frames = [open('app/static/' + f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    def get_frame(self):
        return self.frames[int(time()) % 3]