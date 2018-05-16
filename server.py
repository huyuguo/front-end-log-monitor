from flask import Flask, url_for, request, render_template, session, redirect
app = Flask(__name__)


@app.before_request
def before_login():
  print(request)
  if 'username' in session:
    # return redirect(url_for('index'))
    return 'logined'
  else:
    return 'unlogined'
    # return redirect(url_for('index'))

@app.route('/')
def index():
  return render_template('index.html', name='huyuguo')

@app.errorhandler(404)
def not_found(error):
  return 'This page does not exist', 404

if __name__ == '__main__':
  app.run(debug=True)