from pymongo import MongoClient
from .config import MONGODB_NAME, MONGODB_PORT
from bson.objectid import ObjectId

class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_NAME, MONGODB_PORT)
        self.db = self.client.DummyApi

    def register_user(self, username):
        userCollection = self.db[username]
        newData = [
            {
                'title': 'Army Of Stone',
                'author': 'Sawyer Moore'
            },
            {
                'title': 'Gods Of Dusk',
                'author': 'Kennedy Simpson'
            },
            {
                'title': 'Call To The Apocalypse',
                'author': 'Ainsley Moore'
            }
        ]
        userCollection.insert_many(newData)
        data = []
        documents = userCollection.find()
        for document in documents:
            document['_id'] = str(document['_id'])
            data.append(document)
        return data

    def documents_in_username(self, username):
        return self.db[username].find()
    
    def list_collection_names(self):
        return self.db.list_collection_names()
    
    def find_one_id(self, username, id):
        return self.db[username].find_one({"_id": ObjectId(id)})
    
    def insert_one(self, username, json_data):
        return self.db[username].insert_one(json_data)
    
    def update_one(self, username, json_data, id):
        return self.db[username].update_one({'_id': self.find_one_id(username, id)['_id']}, {'$set': json_data})
    
    def delete_one(self, username, id):
        return self.db[username].delete_one({"_id": str(id)})

    def get_db(self):
        return self.db