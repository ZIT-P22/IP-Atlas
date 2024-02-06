from flask import Flask
import secrets
from routes import atlas, settings


atlasapp = Flask(__name__, static_folder="static", template_folder="templates")
atlasapp.secret_key = secrets.token_hex(16)

# ? Blueprints
atlasapp.register_blueprint(atlas.bp_atlas)
atlasapp.register_blueprint(settings.bp_settings)


if __name__ == "__main__":
    atlasapp.run(debug=True, host="0.0.0.0", port=5000)
