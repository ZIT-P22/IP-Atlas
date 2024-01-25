from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from helper import *

bp_atlas = Blueprint('atlas', __name__)

@bp_atlas.route('/')
def index():
    return render_template('ip/list.html')

@bp_atlas.route('/ip/list')
def list():
    createJson()
    # printJson()
    data = loadJson()
    return render_template('ip/list.html', data=data)

@bp_atlas.route('/ip/<id>')
def show(id):
    createJson()
    data = getHostById(id)
    return render_template('ip/show.html', data=data)

# add new host
@bp_atlas.route('/ip/add')
def add():
    return render_template('ip/add.html')


@bp_atlas.route('/ip/save', methods=['POST'])
def save():
    
    name = request.form.get('name')
    ipv4 = request.form.get('ipv4')
    ipv6 = request.form.get('ipv6')
    ports = request.form.get('ports')
    
    # convert ports from comma sepperated to list
    ports = ports.split(',')
    
    print(name, ipv4, ipv6, ports)
    
    return render_template('ip/add.html')
