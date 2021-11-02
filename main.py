
import generator
from database import _setup
from database import Db
from database import _delete_entries_content
import time

# _setup('ski')
_delete_entries_content()

g = generator.Generator(100)
g.run()


# with Db('ski') as db:
# 	card_id = 5

# 	query = '''INSERT INTO entries (card_id, scanning_time)
# 				VALUES (?, ?)'''
# 	parameters = [card_id,time.ctime()]
# 	db.execute_query(query, parameters)		

