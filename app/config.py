from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
BACK_HOST = os.environ.get("BACK_HOST")
BACK_PORT = os.environ.get("BACK_PORT")
FRONT_HOST = os.environ.get("FRONT_HOST")
FRONT_PORT = os.environ.get("FRONT_PORT")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
DATE_TIME_FORMAT = os.environ.get("DATE_TIME_FORMAT")
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
TITLE = os.environ.get("TITLE")
