import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    ADMIN_USER = os.environ.get('ADMIN_USER')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
