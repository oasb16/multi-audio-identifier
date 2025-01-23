import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)

def train_model():
    data_dir = "data/samples"
    labels = []
    features = []

    for file in os.listdir(data_dir):
        if file.endswith(".wav"):
            label = file.split(".")[0]  # Extract label from filename
            labels.append(label)
            features.append(extract_features(os.path.join(data_dir, file)))

    X = np.array(features)
    y = np.array(labels)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    joblib.dump(model, "models/situation_classifier.pkl")
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    train_model()
