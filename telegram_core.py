import telebot
from sub.constants import Constants as CT
import data_base_instructions
import user_instructions
from sub.option_permission import Jumper
import sub.wrapper

bot = telebot.TeleBot(CT.TELERGAM_API)


class Keyboards:

	@staticmethod
	def search_add_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.SEARCH_ICON, callback_data=CT.BUTTON_SEARCH),
			telebot.types.InlineKeyboardButton(text=CT.ADD_CONTACT_ICON, callback_data=CT.BUTTON_ADD),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data=CT.BUTTON_CLOSE))
		return keyboard

	@staticmethod
	def back_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.BACK_ICON, callback_data=CT.BUTTON_BACK),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data=CT.BUTTON_CLOSE))
		return keyboard

	@staticmethod
	def save_remove():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.SAVE_CONTACT_ICON, callback_data=CT.BUTTON_DOWNLOAD),
			telebot.types.InlineKeyboardButton(text=CT.REMOVE_ICON, callback_data=CT.BUTTON_REMOVE))
		return keyboard

	@staticmethod
	def save_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.ADD_NEW_CONTACT_ICON, callback_data=CT.BUTTON_SAVE_NEW_CONTACT),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data=CT.BUTTON_CLOSE))
		return keyboard

	@staticmethod
	def back_add_close():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.BACK_ICON, callback_data=CT.BUTTON_BACK),
			telebot.types.InlineKeyboardButton(text=CT.ADD_CONTACT_ICON, callback_data=CT.BUTTON_ADD),
			telebot.types.InlineKeyboardButton(text=CT.CLOSE_ICON, callback_data=CT.BUTTON_CLOSE))
		return keyboard

	@staticmethod
	def back_approve_removing():
		keyboard = telebot.types.InlineKeyboardMarkup()
		keyboard.row(
			telebot.types.InlineKeyboardButton(text=CT.BACK_ICON, callback_data=CT.BUTTON_BACK),
			telebot.types.InlineKeyboardButton(text=CT.APPROVE_REMOVING_ICON, callback_data=CT.BUTTON_APPROVE_REMOVING))
		return keyboard


@bot.message_handler(commands=['start'])
@sub.wrapper.set_approve()
def send_welcome(query):
	bot.send_message(query.chat.id, text=CT.START_MESSAGE, reply_markup=Keyboards.search_add_close())


@bot.callback_query_handler(func=lambda c: c.data == CT.BUTTON_BACK)
@sub.wrapper.set_approve()
def callback_return_welcome(query):
	bot.edit_message_text(text=CT.START_MESSAGE, chat_id=query.message.chat.id, message_id=query.message.message_id,
	                      reply_markup=Keyboards.search_add_close())


@bot.callback_query_handler(func=lambda query: query.data == CT.BUTTON_CLOSE)
@sub.wrapper.set_approve()
def callback_worker_exit(query):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)


@bot.callback_query_handler(func=lambda query: query.data == CT.BUTTON_SEARCH)
@sub.wrapper.set_approve(approve_search=True)
def callback_search_menu(query):
	bot.edit_message_text(text=CT.SEARCH_MESSAGE, chat_id=query.message.chat.id, message_id=query.message.message_id,
	                      reply_markup=Keyboards.back_close())


@bot.message_handler(func=lambda query: Jumper.search_contact_status)
@sub.wrapper.set_approve()
def callback_search_result(query):
	results = data_base_instructions.ContactsBase.search_contact_by_request(query.text)
	try:
		if not results[0]:
			bot.send_message(chat_id=query.chat.id, text=user_instructions.send_not_found_message(results[1]))
		else:
			for row in results:
				bot.send_message(chat_id=query.chat.id, text=' '.join(row), reply_markup=Keyboards.save_remove())
	except Exception:
		print(Exception)


@bot.callback_query_handler(func=lambda query: query.data == CT.BUTTON_ADD)
@sub.wrapper.set_approve(approve_add=True)
def add_new_contact_menu_callback_worker(query):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
	bot.send_message(text=CT.ADD_CONTACT_MESSAGE, chat_id=query.message.chat.id, reply_markup=Keyboards.back_close())


@bot.message_handler(func=lambda query: Jumper.add_contact_status)
@sub.wrapper.set_approve()
def callback_user_input_contact_message(query):
	try:
		name, organization, division, job_title, phone, description = query.text.split('\n')
		result = user_instructions.send_new_contact_message(name, organization, division, job_title, phone, description)
		Jumper.add_new_contact_data(result[1])
		bot.send_message(text=result[0], chat_id=query.chat.id, reply_markup=Keyboards.save_close())
	except ValueError:
		bot.send_message(text=CT.ADD_CONTACT_ERROR_MESSAGE, chat_id=query.chat.id,
		                 reply_markup=Keyboards.back_add_close())


@bot.callback_query_handler(func=lambda query: query.data == CT.BUTTON_SAVE_NEW_CONTACT)
@sub.wrapper.set_approve()
def callback_save_contact_to_database(query: telebot.types.CallbackQuery):
	bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
	data_base_instructions.ContactsBase.create_new_contact_with_data(*Jumper.new_contact_data)
	bot.answer_callback_query(callback_query_id=query.id, text=CT.ADD_NEW_CONTACT_TO_ADDRESS_BOOK_SUCCESS_TEXT,
	                          cache_time=10)
	Jumper.add_new_contact_data(False)


@bot.callback_query_handler(func=lambda query: query.data == CT.BUTTON_REMOVE)
@sub.wrapper.set_approve(approve_remove=True)
def callback_remove_contact_menu(query):
	Jumper.removing_number = query.message.text.split()[0]
	bot.edit_message_text(text=query.message.text, chat_id=query.message.chat.id,
	                      message_id=query.message.message_id, reply_markup=Keyboards.back_approve_removing())


@bot.callback_query_handler(func=lambda query: query.data == CT.BUTTON_APPROVE_REMOVING)
@sub.wrapper.set_approve()
def callback_remove_contact_menu_apply(query):
	try:
		data_base_instructions.ContactsBase.remove_contact_with_number(Jumper.removing_number)
		bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
		bot.answer_callback_query(callback_query_id=query.id, text=CT.ERASE_CONTACT_MESSAGE, cache_time=10)
	except Exception:
		print(Jumper.removing_number)


@bot.callback_query_handler(func=lambda query: query.data == CT.BUTTON_DOWNLOAD)
@sub.wrapper.set_approve()
def callback_download_contact_to_phone(query):
	contact_to_download = data_base_instructions.ContactsBase.download_contact_to_phone(query.message.text.split()[0])
	bot.send_contact(chat_id=query.message.chat.id, first_name=contact_to_download[0], phone_number=contact_to_download[1])


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_inline_contact_variations(query):
	variations_list = data_base_instructions.ContactsBase.search_contact_by_request(query.query)
	answer = []
	if not variations_list[0]:
		answer = [telebot.types.InlineQueryResultArticle(
			id=CT.INLINE_ANSWER_EMPTY['id'],
			title=CT.INLINE_ANSWER_EMPTY['title'],
			description=CT.INLINE_ANSWER_EMPTY['description'],
			thumb_url=CT.INLINE_ANSWER_EMPTY['thumb_url'],
			thumb_width=CT.INLINE_ANSWER_EMPTY['thumb_width'],
			thumb_height=CT.INLINE_ANSWER_EMPTY['thumb_height'],
			input_message_content=telebot.types.InputTextMessageContent(
				message_text=user_instructions.send_not_found_message(query.query)
			))]
	else:
		if len(variations_list) > 20:
			answer = [telebot.types.InlineQueryResultArticle(
				id=CT.INLINE_ANSWER_MANY['id'],
				title=CT.INLINE_ANSWER_MANY['title'],
				description=CT.INLINE_ANSWER_MANY['description'],
				thumb_url=CT.INLINE_ANSWER_MANY['thumb_url'],
				thumb_width=CT.INLINE_ANSWER_MANY['thumb_width'],
				thumb_height=CT.INLINE_ANSWER_MANY['thumb_height'],
				input_message_content=telebot.types.InputTextMessageContent(
					message_text=user_instructions.send_many_founded_contact_message(query.query)
				))]
		else:
			for index in range(len(variations_list)):
				answer.append(telebot.types.InlineQueryResultArticle(
					id=str(index + 1),
					title=variations_list[index][1],
					description=variations_list[index][5],
					thumb_url=CT.INLINE_ANSWER_PRETTY['thumb_url'],
					thumb_width=CT.INLINE_ANSWER_PRETTY['thumb_width'],
					thumb_height=CT.INLINE_ANSWER_PRETTY['thumb_height'],
					input_message_content=telebot.types.InputTextMessageContent(
						message_text=' '.join(variations_list[index][1:])
					)))
	bot.answer_inline_query(query.id, answer, cache_time=10)

while True:
	bot.polling(none_stop=True, interval=0, timeout=0)
