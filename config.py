import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-to-a-random-secret")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///
{BASE_DIR / 'instance' / 'app.sqlite'}")
SQLALCHEMY_TRACK_MODIFICATIONS = False
