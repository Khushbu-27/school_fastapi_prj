
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import dbconfig

dbconnconfig = dbconfig()

engine = create_engine(dbconnconfig.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit= False, autoflush= False )

Base = declarative_base() 

def get_db():
    
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()