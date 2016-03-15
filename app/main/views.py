from flask import render_template, session, redirect, url_for, current_app
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User, Cameras
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    cameras = Cameras.query.all()
    return render_template('index.html', cameras=cameras)


