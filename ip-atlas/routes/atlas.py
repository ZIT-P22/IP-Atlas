from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from helper import *

bp_atlas = Blueprint('atlas', __name__)

@bp_atlas.route('/')
def index():
    return render_template('ip/list.html')

@bp_atlas.route('/ip/list')
def list():
    # printJson()
    data = loadJson()
    return render_template('ip/list.html', data=data)

@bp_atlas.route('/ip/<id>')
def show(id):
    data = getHostById(id)
    return render_template('ip/show.html', data=data)