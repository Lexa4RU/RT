import os

class Config:
    SECRET_KEY = "change-me"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://tp_user:tp_password@127.0.0.1/tp_platform"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
