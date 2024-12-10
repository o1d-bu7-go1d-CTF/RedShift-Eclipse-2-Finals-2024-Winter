# Checker (Auth) for Keeyb
# Author: o1d_bu7_go1d

import os
import aiohttp
import asyncio
from colorama import Fore, Style

from keeyb_checker__helper import create_account, connection_check, register_user


# Функция для авторизации пользователя
async def login_check(HOST, PORT, account):
	url = f'http://{HOST}:{PORT}/?action=login'
	try:
		async with aiohttp.ClientSession() as session:
			login_data = {
				"username": account[0],
				"password": account[1],
			}
			async with session.post(url, data=login_data) as user_login:
				if user_login.status == 200 or user_login.status == 302:
					print(Fore.GREEN + f"[+] Checker 1 (Keeyb): {HOST}:{PORT} - login successful" + Style.RESET_ALL)
					return 101, None
				else:
					return 104, None
	except:
		print(Fore.RED + f"[-] Checker 1 (Keeyb): {HOST}:{PORT} - login failed" + Style.RESET_ALL)
		return 104, None


# Агрегирующая функция для остальных
async def checker_login_register(HOST, PORT):
	# 1. Тестовое подключение к сервису
	test_connection = await connection_check(HOST, PORT)

	# 2. Проверяем внутренний статус код из test_connection
	if test_connection[0] == 101:
		# 3. Создаем аккаунт
		account = await create_account()

		# 4. Регистрируем пользователя
		reg_user = await register_user(HOST, PORT, account)

		# 5. Проверяем внутренний статус код из reg_user
		if reg_user[0] == 101:
			# 6. Конечный результат вернется после авторизации и проверки работоспособности
			auth_user = await login_check(HOST, PORT, account)
			if auth_user[0] == 101:
				return 101, None
			else:
				return 104, None
		else:
			return 104, None
	else:
		return 104, None


# Функция, затрагиваемая чек-системой
async def pwn(HOST, PORT):
	VERDICT = await checker_login_register(HOST, PORT)
	print(VERDICT)
	return VERDICT


loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost', 8000))