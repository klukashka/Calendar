from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Boolean, DateTime

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

note = Table(
    "note",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("remind_time", String, nullable=False),
    Column("message", String, nullable=True),
    Column("important", Boolean, nullable=True),
    Column("is_completed", Boolean, nullable=False)
)
