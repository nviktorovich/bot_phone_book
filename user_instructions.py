import data_base_instructions as DB
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


def check_new_contact_message(name, organization, division, job_title, phone, description):
	return (f'Данные контакта:\nИмя: \t[{name}]\nОрганизация: \t[{organization}]\nПодразделение: \t[{division}]'
	        f'\nДолжность: \t[{job_title}]\nТелефон: \t[{phone}]\nДополнительно: \t[{description}]\nСохранить?',
	        (DB.get_number(), name, organization, division, job_title, phone, description)
	        )
