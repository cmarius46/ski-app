
from database import Db
from queue import SimpleQueue, Queue
import time
import random

skidb = Db('ski')

class Generator:

	_exit_factor = 0.5 # from 0 to 1
	_enter_factor = 0.3 # from 0 to 1

	_waiting_time = 0.7 # seconds
	_skiing_time = 1.3 # seconds
	_entering_time = 0.5 # seconds

	def __init__(self, no_ids):
		self._out_of_circuit = [i for i in range(no_ids)]
		self._waiting_q = Queue()
		self._skiing_q = Queue()
		self._last_time_waiting = time.time()
		self._last_time_skiing = time.time()
		self._last_time_entering = time.time()


	def _enter_waiting_q_from_outside(self):
		# entering waiting q from outside
		if len(self._out_of_circuit) > 0:
			# we have people that could enter the waiting q (that are not skiing already)
			enter_probab = random.random()
			if enter_probab > self._enter_factor:
				pos_to_enter = random.randrange(len(self._out_of_circuit))
				enter_id = self._out_of_circuit.pop(pos_to_enter)
				self._waiting_q.put_nowait(enter_id)


	def _enter_waiting_q_from_skiing_q(self):
		#entering waiting q from the skiing q
		if not self._skiing_q.empty():
			# we have people skiing 

			finished_skiing = self._skiing_q.get_nowait()

			exit_probab = random.random()
			if exit_probab > self._exit_factor:
				self._out_of_circuit.append(finished_skiing)
			else:
				self._waiting_q.put_nowait(finished_skiing)


	def _insert_into_db(self, db, card_id):
		query = '''INSERT INTO entries (card_id, scanning_time)
					VALUES (?, ?)'''
		parameters = [card_id, time.ctime()]
		db.execute_query(query, parameters)


	def _enter_skiing_q_from_waiting_q(self, db):
		# entering skiing q from waiting q
		if not self._waiting_q.empty():
			# we have ppl waiting

			starts_skiing = self._waiting_q.get_nowait()
			self._skiing_q.put_nowait(starts_skiing)
			self._insert_into_db(db, starts_skiing)


	def _show_current_state(self):
		print('waiting : ')
		print(list(self._waiting_q.queue))
		print()
		print('skiing : ')
		print(list(self._skiing_q.queue))
		print('\n\n')


	def run(self):

		with Db('ski') as db:
			while(True):

				current_time = time.time()


				if current_time - self._last_time_entering >= self._entering_time:
					self._enter_waiting_q_from_outside()
					self._last_time_entering = current_time
					self._show_current_state()

				if current_time - self._last_time_skiing >= self._skiing_time:
					self._enter_waiting_q_from_skiing_q()
					self._last_time_skiing = current_time
					self._show_current_state()

				if current_time - self._last_time_waiting >= self._waiting_time:
					self._enter_skiing_q_from_waiting_q(db)
					self._last_time_waiting = current_time
					self._show_current_state()







