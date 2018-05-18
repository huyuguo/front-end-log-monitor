#coding:utf-8
from app import app, socketio
import route

if __name__ == '__main__':
  socketio.run(app)