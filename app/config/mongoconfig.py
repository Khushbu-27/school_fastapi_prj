
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

mongodb_uri = "mongodb+srv://School_admin:Admin1234@schoolcluster.lwxwt.mongodb.net/?retryWrites=true&w=majority&appName=SchoolCluster"

port= 8000

client = MongoClient(mongodb_uri, port)

db = client.schooldata_db
collection = db["schooldata"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
