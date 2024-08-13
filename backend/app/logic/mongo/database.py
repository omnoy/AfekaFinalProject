import logging
from pymongo import MongoClient
from pymongo.collection import Collection

mongo = None
user_collection = None
public_official_collection = None
generated_post_collection = None
token_blocklist = None

def init_db(app):
    global mongo, user_collection, public_official_collection, generated_post_collection, token_blocklist

    logging.info(f"Connecting to MongoDB at {app.config['MONGO_URI']}")
    mongo = MongoClient(app.config['MONGO_URI'])
    user_collection = mongo.db["users"]
    public_official_collection = mongo.db["public_officials"]
    generated_post_collection = mongo.db["generated_posts"]
    token_blocklist = mongo.db["token_blocklist"]
    
def get_user_collection() -> Collection:
    if user_collection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return user_collection

def get_public_official_collection()  -> Collection:
    if public_official_collection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return public_official_collection
    
def get_generated_post_collection() -> Collection:
    if generated_post_collection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return generated_post_collection

def get_token_blocklist() -> Collection:
    if token_blocklist is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return token_blocklist