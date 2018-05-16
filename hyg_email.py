from flask import Flask
from flask_mail import Mail, Message
import configmodule
import sys

app = Flask(__name__)
if sys.platform == 'darwin':
  app.config.from_object('configmodule.DevelopmentConfig')
else:
  app.config.from_object('configmodule.ProductionConfig')
mail = Mail(app)

@app.route('/')
def index():
  msg = Message(
    subject='一度用车-前端日志监控验证码',
    recipients=['huyuguook@163.com']
  )
  msg.html = 'testinghtml'
  mail.send(msg)
  return 'ok'

if __name__ == '__main__':
  app.run()