from flask import Flask, session
import os
from models import *
from extensions import db, migrate
from routes.atlas import atlas
from routes.settings import settings_bp
from routes.scan import scan
from dotenv import load_dotenv

load_dotenv()

atlasapp = Flask(__name__, static_folder="static", template_folder="templates")

database_dir = os.path.join(os.getcwd(), "database")
if not os.path.exists(database_dir):
    os.makedirs(database_dir)
atlasapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    database_dir, "ip_atlas.db"
)

print(atlasapp.config["SQLALCHEMY_DATABASE_URI"])
atlasapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
atlasapp.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'supersecretkey'

# Register the blueprints
atlasapp.register_blueprint(atlas)
atlasapp.register_blueprint(settings_bp)
atlasapp.register_blueprint(scan)

# Initialize SQLAlchemy with the Flask app
db.init_app(atlasapp)
migrate.init_app(atlasapp, db)

if __name__ == "__main__":
    with atlasapp.app_context():
        from models import *
        db.create_all()
    atlasapp.run(debug=True, host="0.0.0.0", port=5000)
