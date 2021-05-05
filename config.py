import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET KEY') or 'q\xe9J\xf1\x8e K\x9dw\x05A\x9b\x9c\x08s\xd5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False