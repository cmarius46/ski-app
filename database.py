
import sqlite3

class Db:
	def __init__(self, db_name):
		self.db_name = db_name
		try:
			filename = self.db_name + '.db'
			self.connection = sqlite3.connect(filename)
		except sqlite3.Error as error:
			print('Error connecting to ' + str(self.db_name), error)


	def __enter__(self):
		return self.connection


	def __exit__(self):
		self.connection.close()









