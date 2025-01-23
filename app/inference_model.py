import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler
import joblib

def infer_situation(audio_path):
    model = joblib.load("models/situation_classifier.pkl")
    y, sr = librosa.load(audio_path, sr=None)
    
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform([mfcc_mean])
    
    prediction = model.predict(features_scaled)
    
    return prediction[0]
