from sqlalchemy import JSON, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import List

engine = create_async_engine('sqlite+aiosqlite:///db.sqlite3', echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = 'chats'
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    users_tg_ids: Mapped[list] = mapped_column(JSON, default=[])

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)