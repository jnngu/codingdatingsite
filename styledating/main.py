from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import sqlite3
import hashlib
from util import *
from user import *

app = Flask(__name__)
app.secret_key = open('secret_key.txt').read()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
	return 'welcome to homepage'

@app.route('/register')
def register():
	return render_template("registration.html")

@app.route('/process_registration', methods=['POST'])
def process_registration():
	f = request.form
	if not f['username'].isalnum():
		return f"username can only contain letters and numbers"
	L = sql_execute('''SELECT * FROM users WHERE username=?''', (f['username'],))
	print(L)
	if len(L) > 0:
		return f"sorry; username {f['username']} already taken"
	num = sql_execute('''SELECT MAX(id) from users''')
	print(num)
	newid = 1 if len(num) == 0 or num[0][0] == None else 1 + num[0][0]
	sql_execute('''INSERT INTO users VALUES (?,?,?,?,?)''',\
		(newid,f['username'],f['name'],'',hashpw(f['pass']),))
	pfp = request.files['pfp']
	pfp.save('database/pfps/'+f['username'])
	#return f"registered! You are user #{newid}<br>" + render_template("login.html")
	return redirect(url_for('login'))


@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/process_login', methods=['POST'])
def process_login():
	f = request.form
	L = sql_execute('''SELECT name FROM users WHERE username=? AND pass_hash=?''',\
		(f['username'], hashpw(f['pass'])))
	print(L)
	if len(L) == 0 or L[0][0] == None:
		return "sorry, login failed\n" + render_template("login.html")
	user = User(f['username'])
	login_user(user)
	return redirect(url_for('coding_chal'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/code')
@login_required
def coding_chal():
	return render_template("formpg.html")

@app.route('/process_code', methods=['POST'])
@login_required
def process_code():
	user_code = request.form['code_submission']
	return "your code was " + user_code

@app.route('/match')
@login_required
def match():
	print(current_user)
	print(current_user.id)
	return f"hi {current_user.name}, here are your matches"

@app.route('/chat')
@login_required
def chat():
	return "welcome to chat"

if __name__ == '__main__':
	app.run(debug=True)