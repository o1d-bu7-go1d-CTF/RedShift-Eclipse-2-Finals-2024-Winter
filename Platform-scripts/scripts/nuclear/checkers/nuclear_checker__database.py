import os
import asyncio
from pwn import *
from colorama import Fore, Style


async def check_user_role_change(ip, port, username, passwd):
    try:
        # Подключение к серверу
        try:
            connection = remote(ip, port, timeout=10)
            print(Fore.GREEN + f"[+] Checker 2 (Nuclear): {ip}:{port} - connection successfull" + Style.RESET_ALL)
        except:
            print(Fore.RED + f"[-] Checker 2 (Nuclear): {ip}:{port} - connection failed" + Style.RESET_ALL)
            return 104, None  # NO: Не удалось подключиться

        # Вход под учетной записью admin
        connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        connection.sendline("admin".encode('utf-8'))
        connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        connection.sendline("admin".encode('utf-8'))

        # Проверка успешного входа с ролью admin
        response = connection.recvuntil("> ".encode('utf-8'), timeout=10)
        if "Добро пожаловать, admin! Роль: admin" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 2 (Nuclear): {ip}:{port} - admin auth and role response successfull" + Style.RESET_ALL)
        elif "Добро пожаловать, admin! Роль: admin" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 2 (Nuclear): {ip}:{port} - admin auth and role response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Добавление нового пользователя {username}
        connection.sendline("add_user".encode('utf-8'))
        connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        connection.sendline(username.encode('utf-8'))
        connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        connection.sendline(passwd.encode('utf-8'))
        connection.recvuntil("Введите роль (operator/admin): ".encode('utf-8'), timeout=10)
        connection.sendline("admin".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=10)
        if "Пользователь добавлен успешно" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 2 (Nuclear): {ip}:{port} - user {username} adding response successfull" + Style.RESET_ALL)
        elif "Пользователь добавлен успешно" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 2 (Nuclear): {ip}:{port} - user {username} adding response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Закрытие соединения
        connection.close()

        # Вход под учетной записью {username}
        connection = remote(ip, port, timeout=10)
        connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        connection.sendline(username.encode('utf-8'))
        connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        connection.sendline(passwd.encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=10)
        if f"Добро пожаловать, {username}! Роль: admin" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 2 (Nuclear): {ip}:{port} - {username} auth and role response successfull" + Style.RESET_ALL)
        elif f"Добро пожаловать, {username}! Роль: admin" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 2 (Nuclear): {ip}:{port} - {username} auth and role response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Закрытие соединения
        connection.close()

        # Вход под учетной записью admin
        connection = remote(ip, port, timeout=10)
        connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        connection.sendline("admin".encode('utf-8'))
        connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        connection.sendline("admin".encode('utf-8'))

        # Изменение роли {username} на operator
        connection.recvuntil("> ".encode('utf-8'), timeout=10)
        connection.sendline("update_user_role".encode('utf-8'))
        connection.recvuntil("Введите имя пользователя для обновления роли: ".encode('utf-8'), timeout=10)
        connection.sendline(username.encode('utf-8'))
        connection.recvuntil("Введите новую роль (operator/admin): ".encode('utf-8'), timeout=10)
        connection.sendline("operator".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=10)
        if "Роль пользователя успешно обновлена" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 2 (Nuclear): {ip}:{port} - role for {username} - response successfull" + Style.RESET_ALL)
        elif "Роль пользователя успешно обновлена" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 2 (Nuclear): {ip}:{port} - role for {username} - response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Закрытие соединения
        connection.close()

        # Вход под учетной записью {username} с новой ролью operator
        connection = remote(ip, port, timeout=10)
        connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        connection.sendline(username.encode('utf-8'))
        connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        connection.sendline(passwd.encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=10)        
        if f"Добро пожаловать, {username}! Роль: operator" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 2 (Nuclear): {ip}:{port} - {username} auth and role operator response successfull" + Style.RESET_ALL)
        elif f"Добро пожаловать, {username}! Роль: operator" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 2 (Nuclear): {ip}:{port} - {username} auth and role operator response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Закрытие соединения
        connection.close()

        # Вход под учетной записью admin для удаления {username}
        connection = remote(ip, port, timeout=10)
        connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        connection.sendline("admin".encode('utf-8'))
        connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        connection.sendline("admin".encode('utf-8'))

        # Удаление пользователя {username}
        connection.recvuntil("> ".encode('utf-8'), timeout=10)
        connection.sendline("delete_user".encode('utf-8'))
        connection.recvuntil("Введите имя пользователя для удаления: ".encode('utf-8'), timeout=10)
        connection.sendline(username.encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=10)
        if "Пользователь успешно удален" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 2 (Nuclear): {ip}:{port} - {username} delete - response successfull" + Style.RESET_ALL)
        elif "Пользователь успешно удален" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 2 (Nuclear): {ip}:{port} - {username} delete - response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Закрытие соединения
        connection.close()
        return 101, None  # OK: Все проверки успешно выполнены
    except:
        return 104, None  # NO: Ошибка входных данных


async def pwn(HOST):
    username = str(os.urandom(10).hex())
    passwd = str(os.urandom(10).hex())

    VERDICT = await check_user_role_change(HOST, 9000, username, passwd)
    print(VERDICT)
    return VERDICT
