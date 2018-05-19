#coding:utf-8

from  run import app, mail, db
from flask import  request, session, render_template, redirect, url_for, json, flash
from flask_mail import Message
import model
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    res = {
      'status': 0,
      'msg': '注册成功',
      'data': {
      }
    }

    email = request.json.get('email')
    password = request.json.get('password')
    code = request.json.get('code')
    checked = True
    if email == None or len(email) == 0 or len(email) > 60:
      checked = False
      res['status'] = 1
      res['msg'] = '请输入正确的邮箱'
      return json.dumps(res)
    if password == None or len(password) < 8 or len(password) > 16:
      checked = False
      res['status'] = 1
      res['msg'] = '请输入8-16位密码'
      return json.dumps(res)
    if code == None or len(code) != 6:
      res['status'] = 1
      res['msg'] = '请输入正确的验证码'
      return json.dumps(res)

    user = model.User.query.get(email)
    if user == None: # 用户没有进行获取验证码操作
      res['status'] = 1
      res['msg'] = '请输入正确的验证码'
      return json.dumps(res)
    else:
      if user.status == 0:
        if code == user.code:  # 注册成功
          user.password = generate_password_hash(password)
          user.status = 1
          db.session.commit()
          session['logged_in'] = True
          session.permanent = True
        else:
          res['status'] = 1
          res['msg'] = '请输入正确的验证码'
          return json.dumps(res)
      elif user.status == 1:
        res['status'] = 1
        res['msg'] = '用户已注册，请直接登录'
        return json.dumps(res)
      else:
        res['status'] = 1
        res['msg'] = '未知用户状态: %d，请联系管理员' % user.status
        return json.dumps(res)
    return json.dumps(res)
  else:
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  return render_template('login.html')

@app.route('/obtain_code')
def obtain_code():
  res = {
    'status': 0,
    'msg': '邮件已发送，请查看验证码',
    'data': {
    }
  }

  email = str.strip(request.args.get('email'))
  if len(email) == 0:
    res['status'] = 1
    res['msg'] = '请输入正确的邮箱!'
  else:
    user = model.User.query.get(email)
    if user == None:
      user = model.User()
      user.email = email
      code = random.randint(100000, 999999)
      user.code = code
      db.session.add(user)
      db.session.commit()
      send_email(email, code)
    else:
      if user.status == 0:  # 获取验证码
        codetimedelta = datetime.now() - user.updated_time
        # 测试 50分钟
        if codetimedelta.seconds > 50 * 60:  # 超过5分钟更新验证码
          code = random.randint(100000, 999999)
          user.code = code
          db.session.commit()
        else:
          send_email(email, user.code)
      elif user.status == 1:
        res['status'] = 1
        res['msg'] = '该邮件已经注册，请直接登录，或者用其他邮件注册.'
      else:
        res['status'] = 1
        res['msg'] = '用户为位置状态：%d，请联系管理员!' % user.status
  return json.dumps(res)



@app.errorhandler(404)
def not_found(error):
  res = {
    'status': 404,
    'msg': 'This page does not exist',
    'data': {
    }
  }
  return json.dumps(res), 404
  # return 'This page does not exist', 404

# 给用户发送验证码邮件
def send_email(email, code):
  msg = Message(
    subject='消息接收邮箱验证',
    recipients=[email + '@yiduyongche.com']
  )
  msg.body = '【一度用车-前端日志监控】验证码：' + str(code) + ', 该验证码5分钟内有效。为了保障您的账户安全，请勿向他人泄漏验证码信息。'
  mail.send(msg)