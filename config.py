import os
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

class Config:
    # Pobieranie SECRET_KEY ze zmiennej środowiskowej
    # Jeśli nie jest ustawiona, używa wartości domyślnej (tylko do developmentu!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-never-use-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///quiz.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# .env
SECRET_KEY=8f7a89d2e149a4b3c5e9f2d1b6a0c3e7f4d8a5b2c9e6f3d0a7b4c1e8f5d2a9c6
DATABASE_URL=sqlite:///quiz.db