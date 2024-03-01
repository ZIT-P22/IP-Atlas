from flask import Blueprint, render_template, request, abort, jsonify

settings = Blueprint("settings", __name__)


@settings.route("/config")
def config():
    return render_template("settingsPage.html")
