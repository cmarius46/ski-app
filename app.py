
import database
import time


class App:

	def __init__(self):
		self._no_entries_from_db = 500
		self._time_diff_in_seconds = 3600


	def calculate_time(self):

		entries = self._get_entries_from_db(self._no_entries_from_db)
		tim = self._calculate_time_from_entries(entries)

		return tim


	def _get_entries_from_db(self, no_entries):
		query = '''SELECT * 
					FROM entries
					ORDER BY scanning_time DESC
					LIMIT ?'''

		parameters = [no_entries]

		with database.Db('ski') as db:
			entries = db.execute_return_query(query, parameters)

		entries = self._turn_entries_to_dic(entries)

		return entries


	def _turn_entries_to_dic(self, entries):
		entries = [self._entry_to_dic(entry) for entry in entries]

		return entries


	def _entry_to_dic(self, entry):
		names = ['id', 'card_id', 'scanning_time']
		dic = {names[i]: entry[i] for i in range(len(names))}

		return dic
	

	def _sort_entries_key(self, entry):
		return entry['card_id']


	def _make_dic_with_scanning_times(self, entries):
		dic = {}

		for entry in entries:
			try:
				test = dic[entry['card_id']]
			except KeyError:
				dic[entry['card_id']] = []
			finally:
				dic[entry['card_id']].append(entry['scanning_time'])

		return dic


	def _replace_scanning_times_with_diffs(self, dic):
		for card_id in dic:
			diff_list = []
			for i in range(len(dic[card_id])-1):
				# list[i] - list[i+1]

				t2 = time.strptime(dic[card_id][i+1])
				t1 = time.strptime(dic[card_id][i])
				diff = time.mktime(t1) - time.mktime(t2)
				diff_list.append(diff)

			dic[card_id] = diff_list

		return dic


	def _calculate_time_diffs_from_entries(self, entries):
		entries.sort(key=self._sort_entries_key)

		dic = self._make_dic_with_scanning_times(entries)

		dic = self._replace_scanning_times_with_diffs(dic)

		dic = self._delete_empty_keys(dic)
		
		return dic


	def _delete_empty_keys(self, dic):
		for k in list(dic.keys()):
			if len(dic[k]) == 0:
				del dic[k]

		return dic


	def _calculate_time_avg(self, time_diff_dic):
		avg = 0
		count = 0

		for card_id in time_diff_dic:
			for diff in time_diff_dic[card_id]:
				count += 1
				avg += diff

		avg_time = int(round(avg / count, 0))

		return avg_time


	def _calculate_time_from_entries(self, entries):
		time_diff_dic = self._calculate_time_diffs_from_entries(entries)

		avg_time_dif = self._calculate_time_avg(time_diff_dic)

		return avg_time_dif










