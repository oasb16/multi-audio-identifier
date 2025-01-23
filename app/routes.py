from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash
import os
from .audio_analysis import analyze_audio

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/health')
def health_check():
    return "Hello, this is working fine!"

@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "audio" not in request.files:
            flash("No audio file uploaded.")
            return redirect(request.url)

        audio = request.files["audio"]

        if audio.filename == "":
            flash("No selected file.")
            return redirect(request.url)

        audio_path = os.path.join(main_blueprint.root_path, "static/uploads", audio.filename)
        audio.save(audio_path)

        # Process the audio
        print(f"Processing audio file: {audio_path}")
        analysis_result = analyze_audio(audio_path)

        if "error" in analysis_result:
            flash("Error analyzing audio. Please try again.")
        else:
            flash("Audio analysis successful! See results below.")

        return redirect(url_for("main.download_analysis", filename=audio.filename))

    return render_template("index.html")

@main_blueprint.route("/download/<filename>")
def download_analysis(filename):
    analysis_file = os.path.join(main_blueprint.root_path, "static/analysis", filename + ".json")
    return send_from_directory(os.path.join(main_blueprint.root_path, "static/analysis"), filename + ".json", as_attachment=True)
