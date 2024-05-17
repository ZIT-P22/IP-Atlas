from flask import Flask
import os
from models import *
from extensions import db, migrate
from routes.atlas import atlas
from routes.settings import settings_bp
from routes.scan import scan
from dotenv import load_dotenv

# Laden Sie die Umgebungsvariablen
load_dotenv()

atlasapp = Flask(__name__, static_folder="static", template_folder="templates")

# Datenbankverzeichnis erstellen, falls nicht vorhanden
database_dir = os.path.join(os.getcwd(), "database")
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

# Datenbank-URI konfigurieren
atlasapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    database_dir, "ip_atlas.db"
)

print(atlasapp.config["SQLALCHEMY_DATABASE_URI"])
atlasapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Geheimen Schlüssel aus Umgebungsvariablen laden oder Standardwert verwenden
atlasapp.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'DasWasWer-42')

# Blueprints registrieren
atlasapp.register_blueprint(atlas)
atlasapp.register_blueprint(settings_bp)
atlasapp.register_blueprint(scan)

# SQLAlchemy mit der Flask-App initialisieren
db.init_app(atlasapp)
migrate.init_app(atlasapp, db)

# Definieren und hinzufügen eines benutzerdefinierten Filters
@atlasapp.context_processor
def utility_processor():
    def enumerate_filter(iterable, start=0):
        return enumerate(iterable, start)
    return dict(enumerate=enumerate_filter)

if __name__ == "__main__":
    with atlasapp.app_context():
        db.create_all()
    atlasapp.run(debug=True, host="0.0.0.0", port=5000)
