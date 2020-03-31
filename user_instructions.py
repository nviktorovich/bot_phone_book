import data_base_instructions as DB


def send_new_contact_message(name, organization, division, job_title, phone, description):
	return (f'Данные контакта:\nИмя: \t[{name}]\nОрганизация: \t[{organization}]\nПодразделение: \t[{division}]'
	        f'\nДолжность: \t[{job_title}]\nТелефон: \t[{phone}]\nДополнительно: \t[{description}]\nСохранить?',
	        (DB.get_number(), name, organization, division, job_title, phone, description)
	        )


def send_not_found_message(request):
	return f'⚠️ По запросу: "{request}", ничего не удалось найти'


def send_many_founded_contact_message(request):
	return f'⚠️ По запросу: "{request}", больше 20 совпадений, для отображения результатов воспользуйтесь "/start"'
