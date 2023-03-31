from redis.asyncio import Redis, ConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME_AND_USER, DB_PASS

DATABASE_URL = f"mysql+pymysql://{DB_NAME_AND_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME_AND_USER}"

pool = ConnectionPool(host="localhost", port=6379, db=0, decode_responses=True)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis() -> Redis:
    return Redis(connection_pool=pool)
