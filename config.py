from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
ADMIN_EMAIL=os.environ.get("ADMIN_EMAIL")
ADMIN_EMAIL_PASSWORD=os.environ.get("ADMIN_EMAIL_PASSWORD")
SMTP_SERVER=os.environ.get("SMTP_SERVER")
SMTP_PORT=os.environ.get("SMTP_PORT")
SECRET_KEY=os.environ.get("SECRET")
DATE_TIME_FORMAT=os.environ.get("DATE_TIME_FORMAT")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"