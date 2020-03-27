import sqlite3
from sub.constants import Constants as CT


def set_cursor():
	"""

	:return: cursor with database.db
	"""
	con = sqlite3.connect(CT.DB_PATH)
	cursor = con.cursor()
	return cursor


def apply_change(sql):
	"""

	:param sql: sql is a command on SQLite language
	:return: none returned function
	"""
	cursor = set_cursor()
	cursor.execute(sql)
	cursor.execute('COMMIT')
	cursor.close()


def get_database_list():
	"""

	:return: list with all rows in database
	"""
	sql = f'SELECT * from {CT.TABLE_NAME}'
	cursor = set_cursor()
	database_list = cursor.execute(sql)
	return database_list


def get_number():
	"""

	:return: number of new contact in str-type
	"""
	sql = f'SELECT {CT.NUMBER} from {CT.TABLE_NAME}'
	cursor = set_cursor()
	num_list = cursor.execute(sql)

	return str(max([int(x[0]) for x in num_list]) + 1)


class ContactsBase:

	def __init__(self):
		self.status = ''

	@staticmethod
	def search_contact_by_request(request):
		answer = []
		for row in get_database_list():
			if set(request.split()).issubset(set(' '.join(row[1:]).split())):
				answer.append(row[1:])
		cursor = set_cursor()
		cursor.close()
		return answer if len(answer) > 0 else [[f'По запросу "{request}" не удалось ничего найти']]

	def create_new_contact_with_data(self, number, name, organization, division, job_title, phone, description):
		sql = f'''INSERT INTO {CT.TABLE_NAME} 
({CT.NUMBER}, {CT.NAME}, {CT.ORGANIZATION}, {CT.DIVISION}, {CT.JOB_TITLE}, {CT.PHONE}, {CT.DESCRIPTION}) values 
("{number}", "{name}", "{organization}", "{division}", "{job_title}", "{phone}", "{description}")'''
		apply_change(sql)
		self.status = 'done'
		return self.status

	def remove_contact_with_number(self, number):
		sql = f'DELETE FROM {CT.TABLE_NAME} WHERE {CT.NUMBER} = {str(number)}'
		apply_change(sql)
		self.status = 'done'
		return self.status

