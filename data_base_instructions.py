import sqlite3
from sub.constants import ConstantsDB


class ContactsBase:

	def __init__(self):
		self.answer = None

	def set_cursor(self):
		con = sqlite3.connect('base.db')
		cursor = con.cursor()
		print("Successfully Connected to SQLite")
		return cursor

	def find_by_request(self, request):
		sql = f"SELECT * from {ConstantsDB.TABLE_NAME} WHERE " \
		      f"name LIKE '%{request}%' or phone LIKE '%{request}%' or descriptions LIKE '%{request}%'"
		cursor = self.set_cursor()
		cursor.execute(sql)
		self.answer = cursor.fetchall()
		cursor.close()
		return self.answer if len(self.answer) > 0 else ConstantsDB.EMPTY_RESULT_OF_SEARCH

	def create_new_contact(self, name, phone, descriptions):
		sql = f"INSERT INTO {ConstantsDB.TABLE_NAME} " \
		      f"(name, phone, descriptions) values ('{name}', '{phone}', '{descriptions}')"
		cursor = self.set_cursor()
		cursor.execute(sql)
		cursor.execute("COMMIT")
		print(f"Record inserted successfully into {ConstantsDB.TABLE_NAME}")
		cursor.close()


a = ContactsBase()
# a.create_new_contact('Арсений', '89777666891', 'еще один тестовый контакт')
print(a.find_by_request('еще один тестовый контакт'))

a.create_new_contact('Олег', '89777555891', 'еще один тестовый контакт')
