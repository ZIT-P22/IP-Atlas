from flask import Blueprint, render_template, request, abort
from jinja2 import TemplateNotFound
from helper import *
from flask import jsonify

bp_atlas = Blueprint('atlas', __name__)

@bp_atlas.route('/')
def index():
    createJson()
    data = loadJson()
    return render_template('ip/list.html', data=data)

@bp_atlas.route('/ip/list')
def list():
    createJson()
    # printJson()
    data = loadJson()
    return render_template('ip/list.html', data=data)

@bp_atlas.route('/ip/ping/<ip_address>')
def ping_ip(ip_address):
    pingable = is_ip_pingable(ip_address)
    return jsonify({'pingable': pingable})

@bp_atlas.route('/ip/<id>')
def show(id):
    createJson()
    #get type of id
    id = int(id)
    # print("ID:",id,":")
    data = getHostById(id)
    # print("Daten der ID: ", id, " :", data)
    return render_template('ip/show.html', data=data)

# add new host
@bp_atlas.route('/ip/add')
def add():
    return render_template('ip/add.html')


@bp_atlas.route('/ip/save', methods=['POST'])
def save():
    if request.method == 'POST':
        # get form data
        name = request.form.get('name')
        ipv4 = request.form.get('ipv4')
        ipv6 = request.form.get('ipv6')
        ports = request.form.get('ports')

        if ports:
            # convert ports from comma separated to list
            ports = ports.split(',')
        
        #print(name, ipv4, ipv6, ports)
        writeJson(name, ipv4, ipv6, ports)
    return render_template('ip/list.html')



# delete host
@bp_atlas.route('/ip/delete/<id>')
def delete(id):
    id = int(id)
    deleteHost(id)
    print("Host with id: ", id, " deleted")
    return render_template('ip/list.html')


@bp_atlas.route('/port/list')
def port():
    
    return render_template('port/list.html')

@bp_atlas.route('/statistic')
def statistic():
    return render_template('statistic.html')