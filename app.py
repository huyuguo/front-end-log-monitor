from flask import Flask, request, render_template, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
socketio = SocketIO(app)

# TODO
print(config.Config.SQLALCHEMY_DATABASE_URI)
