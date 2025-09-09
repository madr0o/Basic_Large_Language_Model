import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

MYSQL_URL = os.getenv(
    "MYSQL_URL",
    "mysql+pymysql://root:dzaky26@localhost:3306/zoo_animal?charset=utf8mb4"
)

class Base(DeclarativeBase):
    pass

engine = create_engine(
    MYSQL_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=600,
    isolation_level="READ COMMITTED",
)