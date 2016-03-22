from flask import render_template, Response, flash
from flask.ext.login import login_required
from .import camera
from .. import db
from ..models import Cameras
from .forms import EditCameraSettings
import os
import time

if os.getenv('EYECAM_CONFIG') == 'production':
    print("importing pi camera")
    from camera_pi import Camera, CameraThread
else:
    print('importing sim camera')
    from camera_sim import Camera

def gen(camera):
    camera.startStream()
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')   

@camera.route('/settings/<camNum>', methods=['GET', 'POST'])
@login_required
def settings(camNum):

    form = EditCameraSettings()
    
    if form.validate_on_submit():
        print('This is a submit for update to ' + camNum)
        mycamera = Cameras()
        mycamera.cameraName = camNum
        mycamera.resolution = form.resolution.data
        mycamera.vflip = form.vflip.data
        mycamera.hflip = form.hflip.data
        
        mycamera.updateCameraSettings()
        flash('Your camera settings has been updated.')
        return render_template('camera/settings.html', form=form, camNum=camNum)
    
    print('getting camera info')  
    mycamera = Cameras.query.filter_by(cameraName=camNum).first()
    if mycamera is None:
        abort(404)
    else:
        form.resolution.data = mycamera.resolution
        form.vflip.data = mycamera.vflip
        form.hflip.data = mycamera.hflip        
        return render_template('camera/settings.html', form=form, camNum=camNum)
    
@camera.route('/livefeed/<camNum>')
def livefeed(camNum):
    return render_template('camera/livefeed.html', camNum=camNum)

@camera.route('/videofeed/<camNum>')
def videofeed(camNum):
    print "setting up the video feed with " + camNum
    mycamera = Cameras.query.filter_by(cameraName=camNum).first()
    if mycamera is None:
        abort(404)
    else:
        return Response(gen(Camera(mycamera)), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    