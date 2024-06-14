from sqlalchemy import *
from datetime import time, datetime
from sqlalchemy.exc import DBAPIError


class Database:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///db/calendar.db", isolation_level="AUTOCOMMIT"
        )
        self.conn = self.engine.connect()
        self.metadata = MetaData()
        self.users = Table(
            "Users",
            self.metadata,
            Column("ID", Integer(), primary_key=True),
            Column("email", String(200), nullable=False, unique=True),
            Column("password", String(200), nullable=False),
            Column("surname", String(200), nullable=False),
            Column("name", String(200), nullable=False),
        )
