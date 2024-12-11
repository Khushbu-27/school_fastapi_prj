
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sqlalchemy.orm import sessionmaker

Base = declarative_base() 

mongo_uri = "mongodb+srv://admin:Admin1234@schoolcluster.lwxwt.mongodb.net/?retryWrites=true&w=majority&appName=SchoolCluster"

client = MongoClient(mongo_uri, server_api=ServerApi('1'))

db = client.exam_db
collection_name = db["exam_collection"]

# engine2 = create_engine(mongo_uri)
    
# SessionLocal = sessionmaker(bind=engine2, autocommit= False, autoflush= False )
    
# def get_db():
    
#     db = SessionLocal() 
#     try:
#         yield db
#     finally:
#         db.close()