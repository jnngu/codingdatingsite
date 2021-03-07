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
	return render_template("index.html")

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
	sql_execute('''INSERT INTO users VALUES (?,?,?,?,?,?,?,?)''',\
		(newid,f['username'],f['name'],'',hashpw(f['pass']),"","",""))
	pfp = request.files['pfp']
	pfp.save('static/pfps/'+f['username'])
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
	return redirect(url_for('evaluations'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/code/<int:n>')
@login_required
def coding_chal(n):
	if n < 0 or n > 3:
		return "???"
	else:
		question_text = "sample question text for question " + str(n)
		return render_template("code_chall.html",\
			n=n,question_text=question_text,code="def main():",results="No results yet!",done=None)

def autograde(s):
	if len(s.split('\n')) > 1:
		return ("good job!", True)
	return ("not quite", False)

@app.route('/process_code', methods=['POST'])
@login_required
def process_code():
	n = int(request.form['cnum'])
	if n < 0 or n > 3:
		return "???"
	else:
		question_text = "sample question text for question " + str(n)
		user_code = request.form['code_submission']
		results, passed = autograde(user_code)
		if passed:
			current_user.updatedb(n,user_code)
		return render_template("code_chall.html",n=n,question_text=question_text,code=user_code,results=results,done=passed)

@app.route('/matches')
@login_required
def matches():
	if current_user.numdone() < 3:
		return render_template("matches.html",user=current_user)

	best_match = current_user.compute_best_match()
	return render_template("matches.html",user=best_match)

@app.route('/evaluations')
@login_required
def evaluations():
	return render_template("evaluations.html",user=current_user)

@app.route('/profile')
@login_required
def profile():
	return render_template("profile.html", user=current_user, isMe=True)

@app.route('/chat')
@login_required
def chat():
	return "welcome to chat"

if __name__ == '__main__':
	app.run(debug=True)