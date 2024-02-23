from flask import Flask
import os
from database import db

atlasapp = Flask(__name__, static_folder="static", template_folder="templates")

# Configure the database URI
database_dir = os.path.join(os.getcwd(), "database")
if not os.path.exists(database_dir):
    os.makedirs(database_dir)
atlasapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    database_dir, "ip_atlas.db"
)
atlasapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Register the blueprints
from routes.atlas import bp_atlas
from routes.settings import bp_settings
from routes.scan import bp_scan

atlasapp.register_blueprint(bp_atlas)
atlasapp.register_blueprint(bp_settings)
atlasapp.register_blueprint(bp_scan)


# Initialize SQLAlchemy with the Flask app
db.init_app(atlasapp)

if __name__ == "__main__":
    with atlasapp.app_context():
        from models import *

        db.create_all()
    atlasapp.run(debug=True, host="0.0.0.0", port=5000)
