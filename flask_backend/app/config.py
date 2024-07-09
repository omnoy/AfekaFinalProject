import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_SECRET_KEY='supersecrettopsecret'
    SECRET_KEY = 'flasksecret'
    MONGO_URI = 'mongodb://localhost:27017/statementGenDB'
    TESTING=False