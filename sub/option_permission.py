class Jumper:
	status = False
	add_contact = False

	@staticmethod
	def set_search_permission(setting=False):
		if setting:
			Jumper.status = True
		else:
			Jumper.status = False

	@staticmethod
	def set_add_contact_permission(setting=False):
		if setting:
			Jumper.add_contact = True
		else:
			Jumper.add_contact = False
