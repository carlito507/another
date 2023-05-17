import os


class Config:
    MONGO_URI = os.environ.get('MONGODB_URI').replace("?", "database?")
    SECRET_KEY = os.environ.get('FERNET_KEY')
    JWT_SECRET_KEY = os.environ.get('FERNET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 30
    JWT_REFRESH_TOKEN_EXPIRES = 30

