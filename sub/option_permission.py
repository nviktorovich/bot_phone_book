class Jumper:
	status = False

	@staticmethod
	def set_search_permission(setting=False):
		if setting:
			Jumper.status = True
		else:
			Jumper.status = False
