import os
from dotenv import load_dotenv

# Membaca file .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "kunci-rahasia-portfolio-flask-2026"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "portfolio.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    SUPABASE_URL = os.getenv("SUPABASE_URL")

    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")