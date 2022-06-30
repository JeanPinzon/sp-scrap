import pymongo
import os

mongo_client = pymongo.MongoClient(os.environ['MONGODB_URI'])

print(mongo_client.list_database_names())