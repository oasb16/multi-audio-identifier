import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "asd"
    UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
    TRANSLATED_FOLDER = os.path.join("app", "static", "translated")
    ALLOWED_EXTENSIONS = {'mp4', 'wav'}
    DEBUG = True
