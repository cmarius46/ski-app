
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
		return self


	def __exit__(self ,type, value, traceback):
		self.connection.close()


	def execute_query(self, query, parameters=None):
		cursor = self.connection.cursor()
		if parameters is not None:
			cursor.execute(query, parameters)
		else:
			cursor.execute(query)
		self.connection.commit()
		cursor.close()


def _setup(db_name):
	setup_query = '''CREATE TABLE entries (
	            id INTEGER PRIMARY KEY,
	            card_id INTEGER,
	            scanning_time datetime);'''

	with Db(db_name) as db:
		db.execute_query(setup_query)

	print('Table created successfully !')


def _delete_entries_table_from_ski():
	delete_query = '''DROP TABLE entries'''

	with Db('ski') as db:
		db.execute_query(delete_query)

	print('Table deleted successfully !')


def _delete_entries_content():
	delete_query = '''DELETE FROM entries'''

	with Db('ski') as db:
		db.execute_query(delete_query)

	print('Table content deleted successfully !')