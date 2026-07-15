import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
   
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kunci-rahasia-portfolio-flask-2026')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'portfolio.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 2 MB
