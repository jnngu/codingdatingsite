from flask_login import UserMixin
from util import *
import random
import os

class User(UserMixin):
	def __init__(self,username):
		self.username = username
		self.id = username

		f = sql_execute('''SELECT name, pic_file,c1,c2,c3 FROM users WHERE username=?''',(username,))
		print(f)
		self.name = f[0][0]
		self.picfile = f[0][1]
		self.description = "blah."
		self.c = list(f[0][2:5])
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
		possibilities = sql_execute('''SELECT username FROM users where username not in (SELECT target from actions where actor=?) AND username <>?''', (self.username, self.username))
		unrejected_possibilities = [x[0] for x in possibilities]
		#print("unrej", unrejected_possibilities)
		percentage_list = []
		f = sql_execute('''SELECT c1,c2,c3 FROM users where username=?''', (self.username,))
		#print("username", self.username)
		code = f[0][1]
		if os.path.exists("file1.py"):
			os.remove("file1.py")
		fu = open("file1.py", "x")
		fu.write(code)
		fu.close()	
		for x in unrejected_possibilities:
			f2 = sql_execute('''SELECT c1,c2,c3 FROM users where username=?''', (x,))
			#print("second user", f2)
			code2 = f2[0][1]
			print("code1", code)
			print("code2", code2)
			if code2 == '':
				perline = 0
			else:
				if os.path.exists("file2.py"):
					os.remove("file2.py")
				fu2 = open("file2.py", "x")
				fu2.write(code2)
				fu2.close()
				os.popen('echo \"file1.py file2.py\" | sml -m sources.cm')
				f3 = open('output', 'r')
				perline = f3.readline()
				perline = 100 - eval(perline)
				#print("line", perline)
			percentage_list += [(perline, x)]
		percentage_list.sort(key = lambda x:x[0], reverse=True)
		print("percentage_list", percentage_list)
		#TODO: currently just returning someone at random (whoever happens to be the first returned).
		# using this list of unrejected possibilities, find the one with the closest vector to ourselves.
		if percentage_list == []:
			return None
		else:
			return User(percentage_list[0][1])

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



	def get_mutual_matches(self):
		mutuals = sql_execute('''SELECT username FROM users where username in (SELECT target from actions where actor=? AND
			act="yes") AND username in (SELECT actor from actions where target=? AND act="yes") ''', (self.username, self.username))
		print(mutuals)
		return [User(x[0]) for x in mutuals]




