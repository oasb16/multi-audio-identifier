import os
from flask import Flask
from app.routes import main_blueprint  # Import blueprint properly

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key_here"
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["ANALYSIS_FOLDER"] = "static/analysis"

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["ANALYSIS_FOLDER"], exist_ok=True)

    app.register_blueprint(main_blueprint)  # Register blueprint correctly

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
