# Checker Helper for MedOK
# Author: boomgarang

import pymysql
import os
import aiohttp
from colorama import Fore, Style

DB_HOST = '192.168.210.114'
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
                    print(Fore.GREEN + "[+] User registered successfully" + Style.RESET_ALL)
                    if resp.cookies:
                        cookies = resp.cookies
                        return 101, (cookies, email)
                    else:
                        print(Fore.RED + "[-] Cookies not found after registration" + Style.RESET_ALL)
                        return 104, None
                else:
                    print(Fore.RED + "[-] User registration failed" + Style.RESET_ALL)
                    return 104, None
        except Exception as e:
            print(Fore.RED + f"[-] Error during registration: {e}" + Style.RESET_ALL)
            return 110, None

async def delete_user_from_db(email):
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (email,))
            connection.commit()
        connection.close()
        print(Fore.GREEN + "[+] User deleted from database" + Style.RESET_ALL)
        return 101, None
    except Exception as e:
        print(Fore.RED + f"[-] Error deleting user: {e}" + Style.RESET_ALL)
        return 110, None

async def delete_appointment(message):
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM appointments WHERE comment = %s", (message,))
            connection.commit()
        connection.close()
        print(Fore.GREEN + "[+] Appointment deleted from database" + Style.RESET_ALL)
        return 101, None
    except Exception as e:
        print(Fore.RED + f"[-] Error deleting appointment: {e}" + Style.RESET_ALL)
        return 110, None