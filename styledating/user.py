from flask_login import UserMixin
from util import *

class User(UserMixin):
	def __init__(self,username):
		self.username = username
		self.id = username

		f = sql_execute('''SELECT name, pic_file,c1,c2,c3 FROM users WHERE username=?''',(username,))
		print(f)
		self.name = f[0][0]
		self.picfile = f[0][1]
		self.c = list(f[0][2:5])
		print("selfc is ", self.c)

		self.num = 3 - (self.c[0] == "") - (self.c[1] == "") - (self.c[2] == "")

	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return self.id

	def numdone(self):
		f = sql_execute('''SELECT c1,c2,c3 FROM users where username=?''', (self.username,))
		return (f[0][0] != "") + (f[0][1] != "") +(f[0][2] != "")

	def compute_best_match(self):
		print(self.name)
		return self
		

	def donewith(self,n):
		if n==1:
			f = sql_execute('''SELECT c1 FROM users where username=?''', (self.username,))
		elif n==2:
			f = sql_execute('''SELECT c2 FROM users where username=?''', (self.username,))
		elif n==3:
			f = sql_execute('''SELECT c3 FROM users where username=?''', (self.username,))
		print("f is ", f)
		return len(f[0][0])
	
	def updatedb(self,n,code):
		f = sql_execute('''select id,username,name,pic_file,pass_hash,c1,c2,c3 from users where username=?''',(self.username,))
		(_id,username,name,picfile,passhash,c1,c2,c3) = f[0]
		sql_execute('''delete from users where username=?''', (username,))
		if n==1:
			sql_execute('''INSERT INTO users VALUES(?,?,?,?,?,?,?,?)''',(_id,username,name,picfile,passhash,code,c2,c3))
		if n==2:
			sql_execute('''INSERT INTO users VALUES(?,?,?,?,?,?,?,?)''',(_id,username,name,picfile,passhash,c1,code,c3))
		if n==3:
			sql_execute('''INSERT INTO users VALUES(?,?,?,?,?,?,?,?)''',(_id,username,name,picfile,passhash,c1,c2,code))