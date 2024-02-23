from flask import Blueprint, render_template, request, abort, jsonify
from utils.helper import *
from utils.filter import *

settings = Blueprint("settings", __name__)


@settings.route("/config")
def config():
    return render_template("settingsPage.html")
