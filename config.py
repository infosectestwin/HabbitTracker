import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        # Generate a secure random key if not provided
        # In production, always set SECRET_KEY environment variable
        SECRET_KEY = secrets.token_hex(32)
        print("WARNING: Using auto-generated SECRET_KEY. Set SECRET_KEY environment variable in production!")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'database.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
