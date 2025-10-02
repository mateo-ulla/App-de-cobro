import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MP_ACCESS_TOKEN = os.environ.get("MERCADOPAGO_ACCESS_TOKEN", "")
    MP_PUBLIC_KEY = os.environ.get("MERCADOPAGO_PUBLIC_KEY", "")
