import asyncio
from pwn import *
from colorama import Fore, Style


async def check_login_admin(ip, port):
    try:
        # Подключение к серверу
        try:
            connection = remote(ip, port, timeout=10)
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - connection successfull" + Style.RESET_ALL)
        except:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - connection failed" + Style.RESET_ALL)
            return 104, None  # NO: Не удалось подключиться

        # Проверка входа под учетной записью admin
        response = connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        if response:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - username admin response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - username admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("admin".encode('utf-8'))

        response = connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        if response:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - admin password response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - admin password response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("admin".encode('utf-8'))

        response = connection.recvline(timeout=10)
        if response:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - auth admin response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - auth admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        response_text = response.decode('utf-8').strip()
        if "Добро пожаловать, admin! Роль: admin" in response_text:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - admin role response successfull" + Style.RESET_ALL)
        elif "Добро пожаловать, admin! Роль: admin" not in response_text:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - admin role response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды exit
        connection.sendline("exit".encode('utf-8'))
        response = connection.recvline(timeout=10)
        if not response or "Завершение программы" not in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - exit response successfull" + Style.RESET_ALL)
            connection.close()
            return 101, None  # Ошибка с exit не является критичной для входа
        connection.close()
    except:
        return 104, None  # NO: Unexpected end of input

async def check_login_operator(ip, port):
    try:
        # Подключение к серверу
        try:
            connection = remote(ip, port, timeout=10)
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - connection successfull" + Style.RESET_ALL)
        except:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - connection failed" + Style.RESET_ALL)
            return 104, None  # NO: Не удалось подключиться

        # Проверка входа под учетной записью operator
        connection = remote(ip, port, timeout=10)

        response = connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=10)
        if response:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - username operator response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - username operator response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("operator".encode('utf-8'))

        response = connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=10)
        if response:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - operator password response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - operator password response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("operator".encode('utf-8'))

        response = connection.recvline(timeout=10)
        if response:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - auth operator response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - auth operator response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        response_text = response.decode('utf-8').strip()
        if "Добро пожаловать, operator! Роль: operator" in response_text:
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - operator role response successfull" + Style.RESET_ALL)
        elif "Добро пожаловать, operator! Роль: operator" not in response_text:
            print(Fore.RED + f"[-] Checker 1 (Nuclear): {ip}:{port} - operator role response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None
        
        # Проверка команды exit
        connection.sendline("exit".encode('utf-8'))
        response = connection.recvline(timeout=10)
        if not response or "Завершение программы" not in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 1 (Nuclear): {ip}:{port} - exit response successfull" + Style.RESET_ALL)
            connection.close()
            return 101, None  # Ошибка с exit не является критичной для входа
        connection.close()

        connection.close()
        return 101, None  # OK: Both logins successful
    except:
        return 104, None  # NO: Unexpected end of input

async def check_login_main(ip, port):
    # Вызов функции для авторизации admin
    admin_login = await check_login_admin(ip, port)

    if admin_login[0] == 101:
        # Если авторизация под админом успешно, то пытаемся авторизоваться дополнительно под operator
        operator_login = await check_login_operator(ip, port)
        return operator_login
    else:
        return 104, None


async def pwn(HOST):
    VERDICT = await check_login_main(HOST, 9000)
    print(VERDICT)
    return VERDICT