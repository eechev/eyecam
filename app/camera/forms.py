from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import Required

class EditCameraSettings(Form):
    resolution = SelectField(u'Resolution', choices=[('low', 'LOW'), ('medium', 'MEDIUM'), ('high', 'HIGH')])
    hflip = BooleanField(u'Horizontal Flip')
    vflip = BooleanField(u'Vertical Flip')
    submit = SubmitField(u'Update')