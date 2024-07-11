import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_SECRET_KEY='supersecrettopsecret'
    SECRET_KEY = 'flasksecret'
    TESTING=False