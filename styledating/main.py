from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import sqlite3
import hashlib
import re
from util import *
from user import *
from autograde import *

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

dct = {1:'pal', 2:'robot', 3:'rotated'}
fcn_names = {1:'palindrome', 2:'judge', 3:'rotate'}

@app.route('/code/<int:n>')
@login_required
def coding_chal(n):
	if n < 1 or n > 3:
		return "???"
	else:
		sc = open("challenges/"+dct[n]+"_sc.py").read()
		question_text = open("challenges/"+dct[n]+"_desc.txt").read().split('\n')
		return render_template("code_chall.html",\
			n=n,question_text=question_text,code=sc,results=["No results yet!"],done=None)

@app.route('/process_language', methods=['POST'])
def process_language():
	n = int(request.form['n'])
	if request.form['language'] == "Python":
		sc = open("challenges/"+dct[n]+"_sc.py").read()
		question_text = open("challenges/"+dct[n]+"_desc.txt").read().split('\n')
		return render_template("code_chall.html",\
			n=n,question_text=question_text,code=sc,results=["No results yet!"],done=None,lang='python')
	else:
		sc = open("challenges/"+dct[n]+"_sc.c").read()
		question_text = open("challenges/"+dct[n]+"_desc.txt").read().split('\n')
		return render_template("code_chall.html",\
			n=n,question_text=question_text,code=sc,results=["No results yet!"],done=None,lang='c')

@app.route('/process_code', methods=['POST'])
@login_required
def process_code():
	n = int(request.form['cnum'])
	if n < 1 or n > 3:
		return "???"
	else:
		question_text = open("challenges/"+dct[n]+"_desc.txt").read().split('\n')
		user_code = request.form['code_submission']
		tc_filename ="challenges/"+dct[n]+"_testcases.txt"
		sol_filename = "challenges/"+dct[n]+"_sol.txt"
		lang = request.form['language']

		(numWrong,results) = runAutograder(lang.lower(),user_code,fcn_names[n],tc_filename, sol_filename)
		results = results.split('\n')

		if numWrong == 0:
			#TODO: user_code is a string with the user's submitted code.
			# current_user.username is the user's username.
			# @ Brandon.
			current_user.updatedb(n,user_code)
		return render_template("code_chall.html",n=n,\
			question_text=question_text,code=user_code,results=results,\
			done=(numWrong == 0))

@app.route('/matches')
@app.route('/matches/<string:typ>/<string:other>')
@login_required
def matches(typ=None,other=None):
	if other != None:
		sql_execute('''insert into actions values(?,?,?)''', (typ,current_user.username,other))

	if current_user.numdone() < 3:
		return render_template("matches.html",user=current_user,curr=current_user)

	best_match = current_user.compute_best_match()
	return render_template("matches.html",user=best_match,curr=current_user)

@app.route('/evaluations')
@login_required
def evaluations():
	return render_template("evaluations.html",user=current_user)

@app.route('/profile')
@login_required
def profile():
	return render_template("profile.html", user=current_user, isMe=True)

@app.route('/mutual')
@login_required
def mutual():
	matches = current_user.get_mutual_matches()
	return render_template("mutual.html", matches=matches, user=current_user)


if __name__ == '__main__':
	app.run(debug=False)
