from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash
import os
from .audio_analysis import analyze_audio

main_blueprint = Blueprint('main', __name__)
print("Template directory path:", os.path.join(main_blueprint.root_path, "templates"))

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

        # Ensure the path is correct and has the right permissions
        audio_path = os.path.join(main_blueprint.root_path, "static/uploads", audio.filename)
        audio.save(audio_path)

        print(f"Audio saved at: {audio_path}")

        # Process the audio
        analysis_result = analyze_audio(audio_path)

        analysis_file = os.path.join(main_blueprint.root_path, "static/uploads", audio.filename.split('.')[0] + ".json")
        print(str(analysis_file))

        # Check if analysis file was created successfully
        if os.path.exists(analysis_file):
            print(f"Analysis JSON created: {analysis_file}")
        else:
            print("ERROR: Analysis file not created!")

        if "error" in analysis_result:
            flash("Error analyzing audio. Please try again.")
        else:
            flash("Audio analysis successful! See results below.")

        return redirect(url_for("main.download_analysis", filename=audio.filename))

    return render_template("index.html")


@main_blueprint.route("/download/<filename>")
def download_analysis(filename):
    analysis_file = os.path.join(main_blueprint.root_path, "static/uploads", filename + ".json")
    if not os.path.exists(analysis_file):
        flash("Requested file not found.")
        return redirect(url_for("main.index") + f"?filename={filename}")

    return send_from_directory(os.path.join(main_blueprint.root_path, "static/uploads"), filename + ".json", as_attachment=True)


from flask import jsonify
import json
@main_blueprint.route("/get_analysis/<filename>")
def get_analysis(filename):
    analysis_file = os.path.join(main_blueprint.root_path, "static/uploads", filename + ".json")
    
    if os.path.exists(analysis_file):
        with open(analysis_file, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "Analysis in progress..."}), 202

