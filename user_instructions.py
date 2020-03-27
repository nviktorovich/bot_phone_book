import data_base_instructions
from sub.constants import Constants as CT


def start_message():
	return CT.START_MESSAGE


def search_message():
	return CT.SEARCH_MESSAGE


def add_new_contact_message():
	return CT.ADD_CONTACT_MESSAGE


def add_new_contact_error_message():
	return CT.ADD_CONTACT_ERROR_MESSAGE


def erase_contact_message():
	return CT.ERASE_CONTACT_MESSAGE


def add_contact(user_rows):
	print(search_message())

