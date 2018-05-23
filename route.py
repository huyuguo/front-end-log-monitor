#coding:utf-8

from  run import app, socketio, mail, db, join_room, emit, disconnect
from flask import  request, session, render_template,json, redirect, abort, url_for
from flask_mail import Message
import model
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
  if 'logged_in' in session:
    return redirect('/show_monitor')
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if 'logged_in' in session:
    return redirect('/show_monitor')
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
    if email == None or len(email) == 0 or len(email) > 60:
      res['status'] = 1
      res['msg'] = '请输入正确的邮箱'
      return json.dumps(res)
    if password == None or len(password) < 8 or len(password) > 16:
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
          session['email'] = email
          session.permanent = True
          return json.dumps(res)
        else:
          res['status'] = 1
          res['msg'] = '请输入正确的验证码'
          return json.dumps(res)
      elif user.status == 1 or user.status == 2:
        res['status'] = 1
        res['msg'] = '用户已注册，请直接登录'
        return json.dumps(res)
      else:
        res['status'] = 1
        res['msg'] = '未知用户状态: %d，请联系管理员' % user.status
        return json.dumps(res)
  else:
    return render_template('register.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
  if 'logged_in' in session:
    return redirect('/show_monitor')
  if request.method == 'POST':
    res = {
      'status': 0,
      'msg': '找回密码成功',
      'data': {
      }
    }

    email = request.json.get('email')
    password = request.json.get('password')
    code = request.json.get('code')
    if email == None or len(email) == 0 or len(email) > 60:
      res['status'] = 1
      res['msg'] = '请输入正确的邮箱'
      return json.dumps(res)
    if password == None or len(password) < 8 or len(password) > 16:
      res['status'] = 1
      res['msg'] = '请输入8-16位密码'
      return json.dumps(res)
    if code == None or len(code) != 6:
      res['status'] = 1
      res['msg'] = '请输入正确的验证码'
      return json.dumps(res)

    user = model.User.query.get(email)
    if user == None:
      res['status'] = 1
      res['msg'] = '用户不存在，请先进行注册'
      return json.dumps(res)
    else:
      if user.status == 0 or user.status == 1 or user.status == 2:
        if code == user.code:  # 重置密码成功
          user.password = generate_password_hash(password)
          db.session.commit()
          session['logged_in'] = True
          session['email'] = email
          session.permanent = True
          return json.dumps(res)
        else:
          res['status'] = 1
          res['msg'] = '请输入正确的验证码'
          return json.dumps(res)
      else:
        res['status'] = 1
        res['msg'] = '未知用户状态: %d，请联系管理员' % user.status
        return json.dumps(res)
  else:
    return render_template('change_password.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'logged_in' in session:
    return redirect('/show_monitor')
  if request.method == 'POST':
    res = {
      'status': 0,
      'msg': '登录成功',
      'data': {
      }
    }

    email = request.json.get('email')
    password = request.json.get('password')
    if email == None or len(email) == 0 or len(email) > 60:
      res['status'] = 1
      res['msg'] = '请输入正确的邮箱'
      return json.dumps(res)
    if password == None or len(password) < 8 or len(password) > 16:
      res['status'] = 1
      res['msg'] = '请输入8-16位密码'
      return json.dumps(res)

    user = model.User.query.get(email)
    if user == None:  # 用户没有进行获取验证码操作
      res['status'] = 1
      res['msg'] = '用户不存，请先进行注册'
      return json.dumps(res)
    else:
      if user.status == 0:
        res['status'] = 1
        res['msg'] = '用户不存，请先进行注册'
        return json.dumps(res)
      elif user.status == 1 or user.status == 2:
        checked = check_password_hash(user.password, password)
        if checked:
          session['logged_in'] = True
          session['email'] = email
          session.permanent = True
          return json.dumps(res)
        else:
          res['status'] = 1
          res['msg'] = '请输入正确的密码'
          return json.dumps(res)
      else:
        res['status'] = 1
        res['msg'] = '未知用户状态: %d，请联系管理员' % user.status
        return json.dumps(res)
  else:
    return render_template('login.html')

@app.route('/obtain_code')
def obtain_code():
  res = {
    'status': 0,
    'msg': '邮件已发送，请查看验证码',
    'data': {
    }
  }


  action = request.args.get('action')
  email = str.strip(request.args.get('email'))
  print(action)
  if action == 'register':
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
          if codetimedelta.seconds > 5 * 60:  # 超过5分钟更新验证码
            code = random.randint(100000, 999999)
            user.code = code
            db.session.commit()
          else:
            send_email(email, user.code)
        elif user.status == 1 or user.status == 2:
          res['status'] = 1
          res['msg'] = '该邮件已经注册，请直接登录，或者用其他邮件注册.'
        else:
          res['status'] = 1
          res['msg'] = '用户为位置状态：%d，请联系管理员!' % user.status
  else:
    if len(email) == 0:
      res['status'] = 1
      res['msg'] = '请输入正确的邮箱!'
    else:
      user = model.User.query.get(email)
      if user == None:
        res['status'] = 1
        res['msg'] = '该用户未注册，请先进行注册'
      else:
        if user.status == 0 or user.status == 1 or user.status == 2:  # 获取验证码
          codetimedelta = datetime.now() - user.updated_time
          if codetimedelta.seconds > 5 * 60:  # 超过5分钟更新验证码
            code = random.randint(100000, 999999)
            user.code = code
            db.session.commit()
          else:
            send_email(email, user.code)
        else:
          res['status'] = 1
          res['msg'] = '用户为位置状态：%d，请联系管理员!' % user.status

  return json.dumps(res)

# 用户管理界面
@app.route('/admin')
def admin():
  if 'logged_in' in session:
    email = session['email']
    if email == 'huyuguo':
      return render_template('admin.html')
    else:
      abort(404)
  else:
    return redirect(url_for('index'))

# 查询所有用户
@app.route('/query_users', methods=['POST'])
def query_users():
  res = {
    'status': 0,
    'msg': '邮件已发送，请查看验证码',
    'data': {
    }
  }
  users = []
  for k, v in enumerate(model.User.query.all()):
    users.append({
      'email': v.email,
      'status': v.status
    })
  res['data']['users'] = users
  return json.dumps(res)

# 通过审核
@app.route('/pass_user', methods=['POST'])
def pass_user():
  res = {
    'status': 0,
    'msg': '邮件已发送，请查看验证码',
    'data': {
    }
  }
  email = request.json.get('email')
  user = model.User.query.get(email)
  user.status = 2
  db.session.commit()
  return json.dumps(res)

# 加入黑名单
@app.route('/add_blacklist', methods=['POST'])
def add_blacklist():
  res = {
    'status': 0,
    'msg': '成功加入黑名单',
    'data': {
    }
  }
  email = request.json.get('email')
  user = model.User.query.get(email)
  user.status = '3'
  db.session.commit()
  return json.dumps(res)

# 当前用户连接查看页面
@app.route('/connect')
def connect():
  if 'logged_in' in session:
    email = session['email']
    if email == 'huyuguo':
      return render_template('connect.html')
    else:
      abort(404)
  else:
    return redirect(url_for('index'))

# 当前用户连接查看接口
@app.route('/query_connect', methods=['POST'])
def query_connect():
  res = {
    'status': 0,
    'msg': '邮件已发送，请查看验证码',
    'data': {
    }
  }
  res['data']['connects'] = app.socket_users
  return json.dumps(res)

@app.route('/show_monitor')
def show_monitor():
  if 'logged_in' in session:
    return render_template('show_monitor.html')
  else:
    return redirect(url_for('index'))

@app.route('/add_log_wx', methods=['POST'])
def add_log_wx():
  req = request.json.get('req', '')
  res = request.json.get('res', '')
  url = request.json.get('url', '')
  uid = request.json.get('uid', '')
  return add_log(req, res, url, uid)


@app.route('/add_log_ios', methods=['POST'])
def add_log_ios():
  req = request.form.get('req', '')
  res = request.form.get('res', '')
  url = request.form.get('url', '')
  uid = request.form.get('uid', '')
  return add_log(req, res, url, uid)

@app.route('/add_log_android', methods=['POST'])
def add_log_android():
  req = request.form.get('req', '')
  res = request.form.get('res', '')
  url = request.form.get('url', '')
  uid = request.form.get('uid', '')
  return add_log(req, res, url, uid)

def add_log(req, res, url, uid):
  if req == '':
    return 'failure'
  if url == '':
    return 'failure'
  if uid == '':
    return 'failure'

  room = None
  for k, v in enumerate(app.socket_users):
    if int(v['uid']) == int(uid):
      room = v['room']

  if room != None:
    socketio.emit('log', {
      'url': url,
      'req': req,
      'res': res
    }, room=room)

  return 'success'


@socketio.on('login')
def handle_login_event(data):
  email = session['email']
  user = model.User.query.get(email)
  if user.status == 1:
    emit('login', {
      'status': 1,
      'msg': '请联系管理员审核通过该账户'
    }, room=request.sid)
    return

  if user.status == 3:
    emit('login', {
      'status': 1,
      'msg': '该账户为黑名单账户，无法进行日志监控'
    }, room=request.sid)
    return

  print(app.socket_users)
  tempUser = None
  for k, v in enumerate(app.socket_users):
    print(v)
    if v['uid'] == data['uid']:
      tempUser = v
      break

  if tempUser == None:
    socketUser = {
      'room': request.sid,
      'email': email,
      'uid': data['uid']
    }
    join_room(request.sid)
    app.socket_users.append(socketUser)
    emit('login', {
      'status': 0,
      'msg': '监控成功'
    }, room=request.sid)
  else:
    if tempUser['uid'] == data['uid'] \
        and tempUser['email'] == email:
      if tempUser['room'] == request.sid:
        emit('login', {
          'status': 0,
          'msg': '监控成功'
        }, room=request.sid)
      else:
        socketUser = {
          'room': request.sid,
          'email': email,
          'uid': data['uid']
        }
        disconnect(tempUser['room'])
        join_room(request.sid)
        app.socket_users.append(socketUser)
        emit('login', {
          'status': 0,
          'msg': '监控成功'
        }, room=request.sid)
    else:
      emit('login', {
        'status': 1,
        'msg': 'uid【' + str(data['uid']) + '】已被用户' + tempUser['email'] + '@yiduyongche.com监控'
      }, room=request.sid)


@socketio.on('disconnect')
def handle_disconnect_event():
  for k, v in enumerate(app.socket_users):
    if v['room'] == request.sid:
      del app.socket_users[k]
      break

@app.errorhandler(404)
def not_found(error):
  res = {
    'status': 404,
    'msg': 'This page does not exist',
    'data': {
    }
  }
  return json.dumps(res), 404


# 给用户发送验证码邮件
def send_email(email, code):
  msg = Message(
    subject='消息接收邮箱验证',
    recipients=[email + '@yiduyongche.com']
  )
  msg.body = '【一度用车-前端日志监控】验证码：' + str(code) + ', 该验证码5分钟内有效。为了保障您的账户安全，请勿向他人泄漏验证码信息。'
  mail.send(msg)