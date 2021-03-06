import sqlite3
import hashlib

def sql_execute(query,args=None):
	conn = sqlite3.connect('database/db.db')
	c = conn.cursor()
	if args:
		c.execute(query, args)
	else:
		c.execute(query)
	res = c.fetchall()
	conn.commit()
	c.close()
	conn.close()
	return res

def hashpw(s):
	return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % (10 ** 8)