#coding:utf-8
from app import app, socketio, db, mail, join_room, send, emit, config
import route
import model

if __name__ == '__main__':
  socketio.run(app, host=config.Config.FLASK_HOST)