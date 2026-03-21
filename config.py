import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file immediately
load_dotenv()

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

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
