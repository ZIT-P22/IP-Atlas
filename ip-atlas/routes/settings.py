from flask import Blueprint, render_template, request, abort, jsonify
from helper import *
from filter import *

bp_settings = Blueprint('settings', __name__)


@bp_settings.route('/config')
def config():
    return render_template('settingsPage.html')