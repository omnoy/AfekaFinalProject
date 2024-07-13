import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_SECRET_KEY='supersecrettopsecret'
    JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(minutes=30)
    SECRET_KEY = 'flasksecret'
    TESTING=False