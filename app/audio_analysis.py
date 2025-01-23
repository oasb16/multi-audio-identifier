import librosa
import json

def analyze_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    rms = librosa.feature.rms(y=y).mean()
    
    analysis_result = {
        "tempo": tempo,
        "spectral_centroid": spectral_centroid,
        "rms_energy": rms
    }
    
    return json.dumps(analysis_result, indent=4)
