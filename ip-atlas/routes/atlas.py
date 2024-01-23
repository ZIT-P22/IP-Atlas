from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from helper import *

bp_atlas = Blueprint('atlas', __name__)

@bp_atlas.route('/ip/list')
def list():
    return render_template('ip/list.html')
    # return render_template('atlas/list.html', liste=get_list())