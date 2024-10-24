from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DB_URL")

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
DATE_TIME_FORMAT = os.environ.get("DATE_TIME_FORMAT")

SMTP_SERVER=os.environ.get("SMTP_SERVER")
SMTP_PORT=os.environ.get("SMTP_PORT")
ADMIN_EMAIL=os.environ.get("ADMIN_EMAIL")
ADMIN_EMAIL_PASSWORD=os.environ.get("ADMIN_EMAIL_PASSWORD")

LOG_LEVEL=os.environ.get("LOG_LEVEL")