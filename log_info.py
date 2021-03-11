
from aiogram import types


async def log_for_mess_handlers(mess:types.Message):
	user_id = mess['from']['id']
	u_log_name = mess['chat']['username']
	date = mess['date']
	text = mess['text']
	for key, value in mess['from']:
		print(f'{key} - {value}')
	print()
	print(date, f'text command = {text}')

