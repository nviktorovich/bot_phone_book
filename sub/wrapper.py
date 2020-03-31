from .option_permission import Jumper


def set_approve(approve_search=False, approve_add=False, approve_remove=False):
	def jumpers_disabler(func):
		def wrap(*args, **kwargs):
			func(*args, **kwargs)
			if approve_search:
				Jumper.set_search_permission(True)
			if not approve_search:
				Jumper.set_search_permission(False)
			if approve_add:
				Jumper.set_add_contact_permission(True)
			if not approve_add:
				Jumper.set_add_contact_permission(False)
			if approve_remove:
				Jumper.remove_contact_with_number(True)
			if not approve_remove:
				Jumper.remove_contact_with_number(False)

		return wrap

	return jumpers_disabler
