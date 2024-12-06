
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Khushi-27@localhost/data_db" 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit= False, autoflush= False )


Base = declarative_base() 
# Base.metadata.create_all(bind=engine)

def get_db():
    
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()