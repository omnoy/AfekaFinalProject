import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'abcbsj'
    MONGO_URI = 'mongodb://localhost:27017/statementGenDB'