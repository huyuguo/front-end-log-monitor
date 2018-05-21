#coding:utf-8
from run import db
from datetime import datetime

class User(db.Model):
  email = db.Column(db.String(60), primary_key=True)
  code = db.Column(db.String(6))
  status = db.Column(db.Integer, default=0) # 0.注册状态 1.注册成功状态 2.管理员审核通过 3.黑名单用户
  created_time = db.Column(db.DateTime, default=datetime.now)
  updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
  password = db.Column(db.String(100))

  def __repr__(self):
    return '<User: %s>' % self.email