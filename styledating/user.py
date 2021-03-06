from flask_login import UserMixin
from util import *

class User(UserMixin):
	def __init__(self,username):
		self.username = username
		self.id = username

		f = sql_execute('''SELECT name, pic_file FROM users WHERE username=?''',(username,))
		self.name = f[0][0]
		self.picfile = f[0][1]

	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return self.id
