import asyncio
from pwn import *
from colorama import Fore, Style


async def check_reactor_functionality(ip, port):
    try:
        # Подключение к серверу
        try:
            connection = remote(ip, port, timeout=5)
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - connection successfull" + Style.RESET_ALL)
        except:
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - connection failed" + Style.RESET_ALL)
            return 104, None  # NO: Не удалось подключиться

        # Логин под учетной записью admin/admin
        response = connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=5)
        if response:
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - username admin response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - username admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("admin".encode('utf-8'))

        response = connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=5)
        if response:
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - password admin response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - password admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("admin".encode('utf-8'))

        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if response and "Добро пожаловать, admin! Роль: admin" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - auth admin response successfull" + Style.RESET_ALL)
        elif not response or "Добро пожаловать, admin! Роль: admin" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - auth admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды initialize
        connection.sendline("initialize".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if "Реактор уже инициализирован" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - init reactor response successfull" + Style.RESET_ALL)
        elif "Реактор уже инициализирован" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - init reactor response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды start
        connection.sendline("start".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if "Реактор запущен" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - start reactor response successfull" + Style.RESET_ALL)
        elif "Реактор запущен" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - start reactor response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды reactor_status
        connection.sendline("reactor_status".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if "Состояние: Работает" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - status reactor response successfull" + Style.RESET_ALL)
        elif "Состояние: Работает" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - status reactor response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды stop
        connection.sendline("stop".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if "Реактор остановлен" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 3 (Nuclear): {ip}:{port} - status reactor response successfull" + Style.RESET_ALL)
        elif "Реактор остановлен" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 3 (Nuclear): {ip}:{port} - status reactor response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Закрытие соединения
        connection.close()
        return 101, None  # OK: Все команды успешно выполнены
    except:
        return 104, None  # NO: Ошибка входных данных


async def pwn(HOST):
    VERDICT = await check_reactor_functionality(HOST, 9000)
    print(VERDICT)
    return VERDICT


loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost'))
