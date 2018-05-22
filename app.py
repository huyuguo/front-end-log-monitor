from flask import Flask, request, render_template, session
from flask_socketio import SocketIO, join_room, send, emit, disconnect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from  datetime import timedelta
import config

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
socketio = SocketIO(app)
mail = Mail(app)

app.socket_users = []

# 设置session的有效期为15天
app.permanent_session_lifetime = timedelta(days=15)