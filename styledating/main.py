from flask import Flask, render_template, request
import sqlite3
import hashlib
from util import *

app = Flask(__name__)

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
	return f"registered! You are user #{newid}<br>" + render_template("login.html")

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
	return f"success! welcome, {L[0][0]}"


@app.route('/code')
def coding_chal():
	return render_template("formpg.html")

@app.route('/process_code', methods=['POST'])
def process_code():
	user_code = request.form['code_submission']
	return "your code was " + user_code

@app.route('/match')
def match():
	return "here are your matches"

@app.route('/chat')
def chat():
	return "welcome to chat"

if __name__ == '__main__':
	app.run(debug=True)