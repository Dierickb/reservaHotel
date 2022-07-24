import os
from dotenv import load_dotenv

load_dotenv()  # carga todo el contenido de .env en variables de entorno


class Config:
    SERVER_NAME = "localhost:7001"
    DEBUG = True

    DATABASE_PATH = "app/database/hotel_book.db"
    DB_TOKEN = os.environ.get("DB_TOKEN", "")  # Para encriptar la base de datos
    ENCRYPT_DB = True

    TEMPLATE_FOLDER = "views/templates/"
    STATIC_FOLDER = "views/static/"
