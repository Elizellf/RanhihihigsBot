__all__ = [
    "User",
    "Dir",
    "Base",
]

# Про ORM-паттерн асинхронного sqlalchemy и модели
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm

# декларативная модель базы данных python
# https://metanit.com/python/database/3.2.php
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DATE, Integer, VARCHAR, Boolean, DateTime
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_table"

    user_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=False)
    reg_date = Column(DATE, default=datetime.now())
    user_role = Column(Boolean, unique=False, nullable=False)
    user_token = Column(VARCHAR(64), unique=False, nullable=True)
    referer_id = Column(Integer, unique=False, nullable=True)
    
class Dir(Base):
    __tablename__ = "Dir_table"

    Dir_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=False, nullable=False)
    Dir_name = Column(VARCHAR(64), unique=False, nullable=False)
    check_date = Column(DateTime, default=datetime.now(timezone.utc), unique=False)
    

    
