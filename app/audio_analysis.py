import librosa
import json
import numpy as np

def analyze_audio(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

        analysis_result = {
            "tempo": float(tempo),
            "beat_frames": beat_frames.tolist(),
            "chroma": chroma.tolist(),
            "spectral_centroid": spectral_centroid.tolist()
        }

        analysis_file = audio_path.replace("uploads", "analysis") + ".json"
        with open(analysis_file, "w") as f:
            json.dump(analysis_result, f, indent=4)

        return analysis_result
    except Exception as e:
        return {"error": str(e)}
