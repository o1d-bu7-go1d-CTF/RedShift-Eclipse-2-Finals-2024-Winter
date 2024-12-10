# Checker Helper for MedOK
# Author: boomgarang

import pymysql
import os
import aiohttp
from colorama import Fore, Style

# DB_HOST = 'localhost'
DB_USER = 'admin'
DB_PASSWORD = 'xxXX2244'
DB_NAME = 'app'

async def register_user(HOST, PORT):
    username = f"user_" + os.urandom(12).hex()
    email = f"{username}@test.com"
    password = "password123"
    
    async with aiohttp.ClientSession() as client_session:
        params = {
            "name": username,
            "email": email,
            "password": password
        }
        try:
            async with client_session.post(f'http://{HOST}:{PORT}/register', data=params) as resp:
                if resp.status in [200, 302]:
                    print(Fore.GREEN + f"[+] Checker (Medok): {HOST} - User registered successfully" + Style.RESET_ALL)
                    if resp.cookies:
                        cookies = resp.cookies
                        return 101, (cookies, email)
                    else:
                        print(Fore.RED + f"[-] Checker (Medok): {HOST} - Cookies not found after registration" + Style.RESET_ALL)
                        return 104, None
                else:
                    print(Fore.RED + f"[-] Checker (Medok): {HOST} - User registration failed" + Style.RESET_ALL)
                    return 104, None
        except Exception as e:
            print(Fore.RED + f"[-] Checker (Medok): {HOST} - Error during registration: {e}" + Style.RESET_ALL)
            return 104, None

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
        print(Fore.GREEN + f"[+] Checker (Medok): {HOST} - User deleted from database" + Style.RESET_ALL)
        return 101, None
    except Exception as e:
        print(Fore.RED + f"[-] Checker (Medok): {HOST} - Error deleting user: {e}" + Style.RESET_ALL)
        return 110, None

async def delete_appointment(message, HOST):
    try:
        connection = pymysql.connect(
            host=HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM appointments WHERE comment = %s", (message,))
            connection.commit()
        connection.close()
        print(Fore.GREEN + f"[+] Checker (Medok): {HOST} - Appointment deleted from database" + Style.RESET_ALL)
        return 101, None
    except Exception as e:
        print(Fore.RED + f"[-] Checker (Medok): {HOST} - Error deleting appointment: {e}" + Style.RESET_ALL)
        return 110, None