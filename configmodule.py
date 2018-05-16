import os
class Config(object):
  DEBUG = False
  TESTING = False
  # EMAIL CONFIG
  MAIL_SERVER = 'smtp.qiye.163.com'
  MAIL_PORT = '465'
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.environ.get('MAIL_NAME')
  MAIL_DEFAULT_SENDER = os.environ.get('MAIL_NAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class ProductionConfig(Config):
  """
  Production configurations
  """
  DEBUG = False

class DevelopmentConfig(Config):
  """
  Development configurations
  """
  DEBUG = True

class TestingConfig(Config):
  """
  Testing configurations
  """
  TESTING = True