import sqlite3
from sub.constants import ConstantsDB


class ContactsBase:
	con = sqlite3.connect('base.db')
	cursor = con.cursor()

	def __init__(self):
		self.answer = None

	def find_by_request(self, request):
		sql = f"SELECT * from book_of_contacts WHERE " \
		      f"name LIKE '%{request}%' or phone LIKE '%{request}%' or descriptions LIKE '%{request}%'"
		self.cursor.execute(sql)
		self.answer = self.cursor.fetchall()
		return self.answer if len(self.answer) > 0 else ConstantsDB.EMPTY_RESULT_OF_SEARCH



a = ContactsBase()
print(a.find_by_request('55'))