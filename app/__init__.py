from flask import Flask
import os
from app.routes import main_blueprint

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.secret_key = "your_secret_key_here"

    # Configure upload folders
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(base_dir, "static/uploads")
    app.config["ANALYSIS_FOLDER"] = os.path.join(base_dir, "static/analysis")

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["ANALYSIS_FOLDER"], exist_ok=True)

    # Register the blueprint
    app.register_blueprint(main_blueprint, url_prefix="/audio")

    return app
