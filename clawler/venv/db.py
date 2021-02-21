from pymongo import MongoClient

uri = '127.0.0.1'
client = MongoClient(host=uri)
db = client['EDAP']

class DB:
    def __init__(self):
        self.db = db

    def insert(self, collection, data):
        self.db[collection].insert(data)

        
    def find_one(self, collection, data=None):
        return self.db[collection].find_one(data)