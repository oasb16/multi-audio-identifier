from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash
import os
from .audio_analysis import analyze_audio
from .inference_model import infer_situation
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "audio" not in request.files:
            flash("No audio file uploaded.")
            return redirect(request.url)

        audio = request.files["audio"]
        if audio.filename == "":
            flash("No selected file.")
            return redirect(request.url)

        filename = secure_filename(audio.filename)
        audio_path = os.path.join("app/static/uploads", filename)
        audio.save(audio_path)

        analysis_result = analyze_audio(audio_path)
        situation = infer_situation(audio_path)

        return render_template("result.html", result=analysis_result, situation=situation)

    return render_template("index.html")

@main_bp.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("app/static/translated", filename, as_attachment=True)
