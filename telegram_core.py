import telebot
from sub.constants import Constants as CT
import data_base_instructions
import user_instructions
from sub.option_permission import Jumper

bot = telebot.TeleBot(CT.TELERGAM_API)


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


class Keyboards:

	@staticmethod
	def search_add_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.SEARCH_ICON, callback_data='search'),
			telebot.types.InlineKeyboardButton(text=CT.ADD_CONTACT_ICON, callback_data='add'),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data='close'))
		return keyboard

	@staticmethod
	def back_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.BACK_ICON, callback_data='back'),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data='close'))
		return keyboard

	@staticmethod
	def save_remove():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.SAVE_CONTACT_ICON, callback_data='save'),
			telebot.types.InlineKeyboardButton(text=CT.REMOVE_ICON, callback_data='remove'))
		return keyboard

	@staticmethod
	def save_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.ADD_NEW_CONTACT_ICON, callback_data='save_new_contact'),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data='close'))
		return keyboard

	@staticmethod
	def back_add_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.BACK_ICON, callback_data='back'),
			telebot.types.InlineKeyboardButton(text=CT.ADD_CONTACT_ICON, callback_data='add'),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data='close'))
		return keyboard

	@staticmethod
	def back_approve_removing():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.BACK_ICON, callback_data='back'),
			telebot.types.InlineKeyboardButton(text=CT.APPROVE_REMOVING_ICON, callback_data='approve_removing'))
		return keyboard


@bot.message_handler(commands=['start'])
@set_approve()
def send_welcome(query):
	bot.send_message(query.chat.id, text=user_instructions.start_message(), reply_markup=Keyboards.search_add_close())


@bot.callback_query_handler(func=lambda c: c.data == 'back')
@set_approve()
def callback_return_welcome(query):
	bot.edit_message_text(text=user_instructions.start_message(), chat_id=query.message.chat.id,
	                      message_id=query.message.message_id,
	                      reply_markup=Keyboards.search_add_close())


@bot.callback_query_handler(func=lambda query: query.data == 'close')
@set_approve()
def callback_worker_exit(query):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)


@bot.callback_query_handler(func=lambda query: query.data == 'search')
@set_approve(approve_search=True)
def callback_search_menu(query):
	bot.edit_message_text(text=CT.SEARCH_MESSAGE, chat_id=query.message.chat.id, message_id=query.message.message_id,
	                      reply_markup=Keyboards.back_close())


@bot.message_handler(func=lambda query: Jumper.search_contact_status)
@set_approve()
def callback_search_result(query):
	results = data_base_instructions.ContactsBase.search_contact_by_request(query.text)
	try:
		if not results[0]:
			bot.send_message(chat_id=query.chat.id, text=CT.NOT_FOUND_CONTACT_MESSAGE+results[1])
		else:
			for row in results:
				bot.send_message(chat_id=query.chat.id, text=' '.join(row), reply_markup=Keyboards.save_remove())
	except Exception:
		print(Exception)


@bot.callback_query_handler(func=lambda query: query.data == 'add')
@set_approve(approve_add=True)
def add_new_contact_menu_callback_worker(query):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
	bot.send_message(text=CT.ADD_CONTACT_MESSAGE, chat_id=query.message.chat.id, reply_markup=Keyboards.back_close())


@bot.message_handler(func=lambda query: Jumper.add_contact_status)
@set_approve()
def callback_user_input_contact_message(query):
	try:
		name, organization, division, job_title, phone, description = query.text.split('\n')
		result = user_instructions.check_new_contact_message(name, organization, division, job_title, phone,
		                                                     description)
		Jumper.add_new_contact_data(result[1])
		bot.send_message(text=result[0], chat_id=query.chat.id, reply_markup=Keyboards.save_close())
	except ValueError:
		bot.send_message(text=CT.ADD_CONTACT_ERROR_MESSAGE, chat_id=query.chat.id,
		                 reply_markup=Keyboards.back_add_close())


@bot.callback_query_handler(func=lambda query: query.data == 'save_new_contact')
@set_approve()
def callback_save_contact_to_database(query: telebot.types.CallbackQuery):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
	data_base_instructions.ContactsBase.create_new_contact_with_data(*Jumper.new_contact_data)
	bot.answer_callback_query(callback_query_id=query.id, text=CT.ADD_NEW_CONTACT_TO_ADDRESS_BOOK_SUCCESS_TEXT,
	                          cache_time=10)
	Jumper.add_new_contact_data(False)


@bot.callback_query_handler(func=lambda query: query.data == 'remove')
@set_approve(approve_remove=True)
def callback_remove_contact_menu(query):
	Jumper.removing_number = query.message.text.split()[0]
	bot.edit_message_text(text=query.message.text, chat_id=query.message.chat.id,
	                      message_id=query.message.message_id, reply_markup=Keyboards.back_approve_removing())


@bot.callback_query_handler(func=lambda query: query.data == 'approve_removing')
@set_approve()
def callback_remove_contact_menu_apply(query):
	try:
		data_base_instructions.ContactsBase.remove_contact_with_number(Jumper.removing_number)
		bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
		bot.answer_callback_query(callback_query_id=query.id, text=CT.ERASE_CONTACT_MESSAGE, cache_time=10)
	except Exception:
		print(Jumper.removing_number)



while True:
	bot.polling(none_stop=True, interval=0, timeout=0)
