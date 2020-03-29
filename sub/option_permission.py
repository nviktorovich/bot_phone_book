class Jumper:
	search_contact_status = False
	add_contact_status = False
	new_contact_data = ''

	@staticmethod
	def set_search_permission(setting=False):
		if setting:
			Jumper.search_contact_status = True
		else:
			Jumper.search_contact_status = False

	@staticmethod
	def set_add_contact_permission(setting=False):
		if setting:
			Jumper.add_contact_status = True
		else:
			Jumper.add_contact_status = False

	@staticmethod
	def add_new_contact_data(data):
		if data:
			Jumper.new_contact_data = data
		else:
			Jumper.new_contact_data = ''
