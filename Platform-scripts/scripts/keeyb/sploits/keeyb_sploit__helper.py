# Sploit Helper for Keeyb
# Author: o1d_bu7_go1d

import os
import aiohttp
import asyncio
from colorama import Fore, Style


# Функция для создания логина и пароля пользователя
async def create_account():
	account = [f"obg-" + os.urandom(8).hex(), os.urandom(10).hex()]
	return account  # Возврат значения в формате массива ["user", "password"]


# Функция для проверки доступности сервиса
async def connection_check(HOST, PORT):
	url = f'http://{HOST}:{PORT}/'
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as check_connection:
				if check_connection.status == 200:
					print(Fore.GREEN + f"[+] Sploit (Keeyb): {HOST}:{PORT} - connection successful" + Style.RESET_ALL)
					return 101, None
	except:
		print(Fore.RED + f"[-] Sploit (Keeyb): {HOST}:{PORT} - connection lost" + Style.RESET_ALL)
		return 102, None


# Функция для регистрации пользователя в системе
async def register_user(HOST, PORT, account):
	url = f'http://{HOST}:{PORT}/?action=register'
	try:
		async with aiohttp.ClientSession() as session:
			reg_data = {
				"username": account[0],
				"password": account[1],
			}
			async with session.post(url, data=reg_data) as user_register:
				if user_register.status == 200 or user_register.status == 302:
					print(Fore.GREEN + f"[+] Sploit (Keeyb): {HOST}:{PORT} - registration successful" + Style.RESET_ALL)
					return 101, None
				else:
					return 102, None
	except:
		print(Fore.RED + f"[-] Sploit (Keeyb): {HOST}:{PORT} - registration failed" + Style.RESET_ALL)
		return 102, None