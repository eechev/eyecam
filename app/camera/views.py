from flask import render_template, Response, flash
from flask.ext.login import login_required
from .import camera
from .. import db
from ..models import Cameras
from .forms import EditCameraSettings
import os

if os.getenv('EYECAM_CONFIG') == 'production':
    from camera_pi import Camera
else:
    from camera_sim import Camera

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@camera.route('/livefeed/<camNum>', methods=['GET', 'POST'])
@login_required
def livefeed(camNum):
    
    form = EditCameraSettings()
    
    if form.validate_on_submit():
        mycamera = Cameras()
        mycamera.cameraName = camNum
        mycamera.resolution = form.resolution.data
        mycamera.vflip = form.vflip.data
        mycamera.hflip = form.hflip.data
        db.session.add(mycamera)
        flash('Your camera settings has been updated.')
        return render_template('camera/livefeed.html', form=form, camNum=camNum)
      
    mycamera = Cameras.query.filter_by(cameraName=camNum).first()
    if mycamera is None:
        abort(404)
    else:
        flash(mycamera.resolution)
        form.resolution = mycamera.resolution
        form.vflip = mycamera.vflip
        form.hflip = mycamera.hflip        
        return render_template('camera/livefeed.html', form=form, camNum=camNum)

@camera.route('/video_feed')
def video_feed():
        return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    