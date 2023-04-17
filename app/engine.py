from os import getenv

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_ENGINE = getenv('DB_ENGINE', None)
DB_USER = getenv('POSTGRES_USER', None)
DB_PASS = getenv('POSTGRES_PASSWORD', None)
DB_NAME = getenv('DB_NAME', None)
DB_HOST = getenv('DB_HOST', None)
DB_PORT = getenv('DB_PORT', None)

if DB_ENGINE:
    engine = create_engine(f'{DB_ENGINE}://{DB_USER}:{DB_PASS}@{DB_HOST}:'
                           f'{DB_PORT}/{DB_NAME}')
else:
    engine = create_engine('sqlite:///mydatabase.db', echo=True)

Session = sessionmaker(engine)
api = FastAPI()
Base = declarative_base()
