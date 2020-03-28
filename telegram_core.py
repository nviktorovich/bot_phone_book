import telebot
from sub.constants import Constants as CT
import data_base_instructions
import user_instructions
from sub.option_permission import Jumper

bot = telebot.TeleBot(CT.TELERGAM_API)


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
	def add_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.ADD_NEW_CONTACT_ICON, callback_data='add_new_contact'),
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





@bot.message_handler(commands=['start'])
def send_welcome(query):
	bot.send_message(query.chat.id, text=user_instructions.start_message(), reply_markup=Keyboards.search_add_close())
	Jumper.set_search_permission(False)
	Jumper.set_add_contact_permission(False)


@bot.callback_query_handler(func=lambda c: c.data == 'back')
def callback_return_welcome(query):
	bot.edit_message_text(text=user_instructions.start_message(), chat_id=query.message.chat.id,
	                      message_id=query.message.message_id,
	                      reply_markup=Keyboards.search_add_close())
	Jumper.set_search_permission(False)
	Jumper.set_add_contact_permission(False)


@bot.callback_query_handler(func=lambda query: query.data == 'close')
def callback_worker_exit(query):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
	Jumper.set_search_permission(False)
	Jumper.set_add_contact_permission(False)


@bot.callback_query_handler(func=lambda query: query.data == 'search')
def callback_search_menu(query):
	bot.edit_message_text(text=CT.SEARCH_MESSAGE, chat_id=query.message.chat.id, message_id=query.message.message_id,
	                      reply_markup=Keyboards.back_close())
	Jumper.set_search_permission(True)
	Jumper.set_add_contact_permission(False)


@bot.message_handler(func=lambda query: Jumper.status)
def callback_search_result(query):
	Jumper.set_search_permission(False)
	Jumper.set_add_contact_permission(False)

	try:
		for row in data_base_instructions.ContactsBase.search_contact_by_request(query.text):
			bot.send_message(chat_id=query.chat.id, text=' '.join(row), reply_markup=Keyboards.save_remove())
	except Exception:
		print(Exception)


@bot.callback_query_handler(func=lambda query: query.data == 'add')
def add_new_contact_menu_callback_worker(query):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
	bot.send_message(text=CT.ADD_CONTACT_MESSAGE, chat_id=query.message.chat.id, reply_markup=Keyboards.back_close())
	Jumper.set_search_permission(False)
	Jumper.set_add_contact_permission(True)


@bot.message_handler(func=lambda query: Jumper.add_contact)
def callback_user_input_contact_message(query):
	try:
		name, organization, division, job_title, phone, description = query.text.split('\n')
		result = user_instructions.check_new_contact_message(name, organization, division, job_title, phone, description)
		print(result)
		bot.send_message(text=result[0], chat_id=query.chat.id, reply_markup=Keyboards.add_close())
	except ValueError:
		bot.send_message(text=CT.ADD_CONTACT_ERROR_MESSAGE, chat_id=query.chat.id, reply_markup=Keyboards.back_add_close())

	Jumper.set_search_permission(False)
	Jumper.set_add_contact_permission(False)


#@bot.callback_query_handler(func=lambda query: query.data == 'add_new_contact')
#def callback_save_contact_to_database(query: telebot.types.CallbackQuery):



while True:
	bot.polling(none_stop=True, interval=0, timeout=0)
