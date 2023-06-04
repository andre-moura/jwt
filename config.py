import os 
import datetime


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    
    # Token expiration time in minutes
    TOKEN_EXPIRATION_MINUTES = 30

    # Calculate token expiration time in seconds
    TOKEN_EXPIRATION_SECONDS = TOKEN_EXPIRATION_MINUTES * 60

    # Calculate token expiration time as a datetime.timedelta object
    TOKEN_EXPIRATION = datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)