import selectors
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("ERROR")
    

engine = create_async_engine(DATABASE_URL, echo=True)
as_session= async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass
async def get_db():
    async with engine.connect() as conn:
       yield conn

#asyncio.run(get_db(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()))
