#coding:utf-8
from app import app, socketio, db, mail
import route
import model

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0')