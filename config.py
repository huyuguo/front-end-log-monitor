import os
class Config(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = os.environ.get('SECRET_KEY')
  FLASK_ENV = os.environ.get('FLASK_ENV')
  FLASK_DEBUG = os.environ.get('FLASK_DEBUG')

  FLASK_HOST = os.environ.get('FLASK_HOST')
  # EMAIL CONFIG
  MAIL_SERVER = 'smtp.qiye.163.com'
  MAIL_PORT = '465'
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.environ.get('MAIL_NAME')
  MAIL_DEFAULT_SENDER = os.environ.get('MAIL_NAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')