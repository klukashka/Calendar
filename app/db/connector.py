from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.base import Base


async def setup_get_pool(db_url: str) -> async_sessionmaker[AsyncSession]:
    """
    Function is used to set up postgres database and create tables if they do not exist.
    Then it connects to database.
    :param db_url: postgres dsn
    :return async_sessionmaker: provides to api an instance how to manage sessions.
    """
    engine = create_async_engine(db_url, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, future=True)

    return async_session_maker