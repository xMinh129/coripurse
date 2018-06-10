import os
import pymongo
from pymongo import MongoClient
from server.models.config import get_config

env_config = get_config()

# Establishing db connection
try:
    conn = pymongo.MongoClient()
    print("Connected to mongo successfully!!!")
except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to mongo: %s" % e)

mongo_host = env_config['mongo']['host']
mongo_port = str(env_config['mongo']['port'])
mongo_db = env_config['mongo']['db']
mongo_user = os.environ.get('MONGO_USER')
mongo_password = os.environ.get('MONGO_PASSWORD')
mongo_connection_str = "mongodb://" + mongo_user + ":" + mongo_password + '@' + mongo_host + ":" + mongo_port + "/" + mongo_db
print("Attempting to connect to " + mongo_connection_str)

client = MongoClient(mongo_connection_str)
db = client[mongo_db]
print("Connected successfully to %s" % db)
if not db:
    print("Failed connecting to %s, bye" % db)
