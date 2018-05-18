#coding:utf-8

from app import app
from flask import  request, session, render_template, redirect, url_for, json

# 登录校验
# @app.before_request
# def before_login():
#   if 'username' not in session: # 未登录， 重定向到默认页面
#     if request.path == '/' or  request.path == '/register' or request.path == '/login':
#       pass
#     else:
#       return redirect(url_for('index'))

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  print(request.form)
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
    res['msg'] = '请输入正确的邮箱'
  else:
    pass
  return json.dumps(res)

@app.errorhandler(404)
def not_found(error):
  return 'This page does not exist', 404