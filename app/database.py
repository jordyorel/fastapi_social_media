from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" #for sql lite
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Establish a database connection (for test purposes)
# while True:
    # try:
    #     conn = psycopg2.connect(
    #         host='localhost',
    #         database='fastapi',
    #         user='postgres',
    #         cursor_factory=RealDictCursor
    #     )
    #     cursor = conn.cursor()
    #     print("Database connection successful!")
    #     break
    # except Exception as error:
    #     print("Connection to the database failed!")
    #     print("Error:", error)
    #     time.sleep(3)
