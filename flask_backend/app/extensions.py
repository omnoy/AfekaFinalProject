from flask_pymongo import PyMongo
from flask_login import LoginManager
from app.generation_model.claude_model import ClaudeModel
from app.models.user import User
from bson import ObjectId

mongo = PyMongo()

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id: str):
    # user_load should not raise an exception if id is not valid
    try:
        user_dict = mongo.db["users"].find_one({"_id":ObjectId(user_id)})
        return User(**user_dict)
    except:
        return None

generation_model = ClaudeModel()