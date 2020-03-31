class Constants:
	TELERGAM_API = '1090271153:AAGZF0toeX9uJ56yv_y1sI94Ghkb2Ku_YNE' # t.me/tester3Bot.
	EMPTY_RESULT_OF_SEARCH = 'No result'
	TABLE_NAME = 'contacts'
	DB_PATH = 'sub/database.db'

	NUMBER = 'number'
	NAME = 'name'
	ORGANIZATION = 'organization'
	DIVISION = 'div'
	JOB_TITLE = 'job_title'
	PHONE = 'tel'
	DESCRIPTION = 'info'

	START_MESSAGE = 'Телефонная книга 📙\n👷‍♂️👮‍♀️👨‍🎓👩‍🏫👩‍🚒'
	SEARCH_MESSAGE = '''Чтобы найти нужный контакт\nотправьте сообщение с данными, 
например:\n- 👤 имя;\n- 👨‍🚀 должность;\n- 🏛 организация, и т.д.'''
	ADD_CONTACT_MESSAGE = 'Введите в одном сообщении с новой строки:' \
	                      '\n- [Название контакта(Имя)];' \
	                      '\n- [Организация/подразделение];' \
	                      '\n- [Отдел/цех];' \
	                      '\n- [Должность];' \
	                      '\n- [Тел: основной];' \
	                      '\n- [Инфо в т.ч доп телефон].'



	ADD_CONTACT_ERROR_MESSAGE = '❗️Необходимо заполнить все шесть полей, каждое поле с новой строки, если поле должно ' \
	                            'быть пустым, ставьте "-" '

	BUTTON_SEARCH = 'search_contact'
	BUTTON_ADD = 'add_new_contact'
	BUTTON_CLOSE = 'close_bot_menu'
	BUTTON_BACK = 'back_to_main_menu'
	BUTTON_DOWNLOAD = 'download_contact_to_phone'
	BUTTON_REMOVE = 'remove_menu'
	BUTTON_APPROVE_REMOVING = 'approve_removing'
	BUTTON_SAVE_NEW_CONTACT = 'save_new_contact'



	ERASE_CONTACT_MESSAGE = 'Контакт стерт 🗑'
	ADD_NEW_CONTACT_TO_ADDRESS_BOOK_SUCCESS_TEXT = '✅Контакт успешно добавлен в адресную книгу'
	NOT_FOUND_CONTACT_MESSAGE = '⚠️ Не удалось найти контакт по запросу: '
	SEARCH_ICON = '🔍'
	ADD_CONTACT_ICON = '📝'
	CLOSE_ICON = '✖️'
	BACK_ICON = '🔙️'
	YES_ICON = '✅'
	REMOVE_ICON = '🗑'
	SAVE_CONTACT_ICON = '💾'
	ADD_NEW_CONTACT_ICON = '➕'
	APPROVE_REMOVING_ICON = '❌'

	INLINE_ANSWER_EMPTY = {'id': '1',
	                       'title': 'Поиск не дал результатов',
	                       'description': 'Попробуйте поменять запрос',
	                       'thumb_url': "https://img.icons8.com/color/48/000000/nothing-found.png",
	                       'thumb_width': 48, 'thumb_height': 48}

	INLINE_ANSWER_MANY = {'id': '1',
	                      'title': 'Много совпадений',
	                      'description': 'Уточните запрос, чтобы уменьшить количество совпадений',
	                      'thumb_url': "https://img.icons8.com/color/48/000000/crowd.png",
	                      'thumb_width': 48, 'thumb_height': 48}

	INLINE_ANSWER_PRETTY = {'id': '',
	                        'title': '',
	                        'description': '',
	                        'thumb_url': "https://img.icons8.com/color/48/000000/contact-card.png",
	                        'thumb_width': 48, 'thumb_height': 48}