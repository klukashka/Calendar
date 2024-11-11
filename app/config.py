"""
WARNING!!!
This module should be used ONCE in main.py
DO NOT use it anywhere else
"""

from dotenv import load_dotenv
from typing import Final
import os
from app.utils.singleton import singleton


@singleton
class AppConfig:
    """
    Build app configuration
    """
    DB_URL: Final[str] = os.environ.get("DB_URL")

    DB_HOST: Final[str] = os.environ.get("DB_HOST")
    DB_PORT: Final[int] = int(os.environ.get("DB_PORT"))
    DB_NAME: Final[str] = os.environ.get("DB_NAME")
    DB_USER: Final[str] = os.environ.get("DB_USER")
    DB_PASS: Final[str] = os.environ.get("DB_PASS")

    BACK_HOST: Final[str] = os.environ.get("BACK_HOST")
    BACK_PORT: Final[int] = int(os.environ.get("BACK_PORT"))
    FRONT_HOST: Final[str] = os.environ.get("FRONT_HOST")
    FRONT_PORT: Final[int] = int(os.environ.get("FRONT_PORT"))
    SECRET_KEY: Final[str] = os.environ.get("SECRET_KEY")

    REDIS_HOST: Final[str] = os.environ.get('REDIS_HOST')
    REDIS_PORT: Final[int] = int(os.environ.get('REDIS_PORT'))
    REDIS_DB: Final[int] = int(os.environ.get('REDIS_DB'))
    REDIS_PASS: Final[str] = os.environ.get("REDIS_PASS")

    DATE_TIME_FORMAT: Final[str] = os.environ.get("DATE_TIME_FORMAT")

    EMAIL_SERVER: Final[str] = os.environ.get("EMAIL_SERVER")
    EMAIL_PORT: Final[int] = int(os.environ.get("EMAIL_PORT"))
    ADMIN_EMAIL: Final[str] = os.environ.get("ADMIN_EMAIL")
    ADMIN_EMAIL_PASSWORD: Final[str] = os.environ.get("ADMIN_EMAIL_PASSWORD")

    LOG_LEVEL: Final[str] = os.environ.get("LOG_LEVEL")
    LOG_FILE: Final[str] = os.environ.get("LOG_FILE")


load_dotenv()
conf = AppConfig()
