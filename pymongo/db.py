from pymongo import MongoClient

def get_db(collection_name=None):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['gym_management']
    
    if collection_name:
        return db[collection_name]
    
    return db
