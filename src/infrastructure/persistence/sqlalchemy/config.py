import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


load_dotenv()

DATABASE = os.getenv('DB_PATH')

DATABASE_URL = f'sqlite:///{DATABASE}'

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
