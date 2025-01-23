import json
import os
import librosa
import numpy as np
import logging
import openai  # Ensure you have the OpenAI package installed

def infer_surroundings(audio_features):
    """Use GPT to infer possible surroundings based on audio features."""
    try:
        # Uncomment this:
        # OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        # openai.api_key = OPENAI_API_KEY
        prompt = (
            f"Consider the following audio characteristics:\n"
            f"Tempo: {audio_features['tempo']} BPM,\n"
            f"RMS Energy: {audio_features['rms_energy']},\n"
            f"Spectral Centroid: {audio_features['spectral_centroid']},\n"
            f"Spectral Bandwidth: {audio_features['spectral_bandwidth']},\n"
            f"Max Pitch: {audio_features['max_pitch']}\n\n"
            f"Don't explain stats, just give brief of the feeling of sound. If a person is sitting in a room, listening to this audio, what would he percieve? Explain to 20 year old person, who cannot hear sounds but needs best description"
        )

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert in audio analysis."},
                      {"role": "user", "content": prompt}]
        )

        inferred_environment = response.choices[0].message.content.strip()
        logging.info(f"Inferred environment: {inferred_environment}")
        return inferred_environment

    except Exception as e:
        logging.error(f"Error in environment inference: {e}")
        return "Inference failed"

def analyze_audio(audio_path):
    try:
        logging.info(f"Analyzing audio file: {audio_path}")

        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)

        # Analyze tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        logging.info(f"Detected tempo: {tempo}")

        # Extract audio features
        rms = float(np.mean(librosa.feature.rms(y=y)))
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        spectral_bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
        pitch, _ = librosa.piptrack(y=y, sr=sr)
        pitch_value = float(np.max(pitch))

        # Prepare analysis result
        analysis_result = {
            "filename": os.path.basename(audio_path),
            "tempo": float(tempo),
            "duration": float(librosa.get_duration(y=y, sr=sr)),
            "rms_energy": rms,
            "spectral_centroid": spectral_centroid,
            "spectral_bandwidth": spectral_bandwidth,
            "max_pitch": pitch_value
        }
        logging.info("Audio feature extraction complete")

        # Infer surroundings using GPT
        analysis_result["environment_inference"] = infer_surroundings(analysis_result)

        # Save analysis result as JSON
        # Save analysis result as JSON
        def safe_serialize(obj):
            if isinstance(obj, np.generic):
                return obj.item()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        analysis_file = os.path.splitext(audio_path)[0] + ".json"
        with open(analysis_file, "w") as f:
            json.dump(analysis_result, f, indent=4, default=safe_serialize)


        return analysis_result

    except Exception as e:
        logging.error(f"Error processing audio: {e}")
        return {"error": str(e)}
