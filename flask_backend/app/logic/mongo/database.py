from flask_pymongo import PyMongo
from pymongo.collection import Collection

mongo = PyMongo()
user_collection = None
po_collection = None
generated_post_collection = None
token_blocklist = None

def init_db(app):
    global mongo, user_collection, po_collection, generated_post_collection, token_blocklist

    mongo.init_app(app)
    user_collection = mongo.db["users"]
    po_collection = mongo.db["public_officials"]
    generated_post_collection = mongo.db["generatedposts"]
    token_blocklist = mongo.db["token_blocklist"]
    
def get_user_collection() -> Collection:
    if user_collection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return user_collection

def get_po_collection()  -> Collection:
    if po_collection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return po_collection
    
def get_generated_post_collection() -> Collection:
    if generated_post_collection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return generated_post_collection

def get_token_blocklist() -> Collection:
    if token_blocklist is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return token_blocklist