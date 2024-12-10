import asyncio
from pwn import *
from colorama import Fore, Style


async def check_reactor_commands(ip, port):
    try:
        # Подключение к серверу
        try:
            connection = remote(ip, port, timeout=5)
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - connection successfull" + Style.RESET_ALL)
        except:
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - connection failed" + Style.RESET_ALL)
            return 104, None  # NO: Не удалось подключиться

        # Логин под учетной записью admin/admin
        response = connection.recvuntil("Введите имя пользователя: ".encode('utf-8'), timeout=5)
        if response:
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - username admin response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - username admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("admin".encode('utf-8'))

        response = connection.recvuntil("Введите пароль: ".encode('utf-8'), timeout=5)
        if response:
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - password admin response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - password admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        connection.sendline("admin".encode('utf-8'))

        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if response and "Добро пожаловать, admin! Роль: admin" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - auth admin response successfull" + Style.RESET_ALL)
        elif not response or "Добро пожаловать, admin! Роль: admin" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - auth admin response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды adjust_rods
        connection.sendline("adjust_rods".encode('utf-8'))
        response = connection.recvuntil("Введите новое положение управляющих стержней (0-100%): ".encode('utf-8'), timeout=5)
        if response:
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - adjust_rods response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - adjust_rods response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None
        
        connection.sendline("10".encode('utf-8'))

        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)        
        if "Управляющие стержни установлены" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - control rods response successfull" + Style.RESET_ALL)
        elif "Управляющие стержни установлены" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - control rods response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды add_coolant
        connection.sendline("add_coolant".encode('utf-8'))
        response = connection.recvuntil("Введите количество охлаждающей жидкости: ".encode('utf-8'), timeout=5)
        if response:
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - add_coolant response successfull" + Style.RESET_ALL)
        elif not response:
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - add_coolant response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None
        connection.sendline("10".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if "Уровень охлаждающей жидкости увеличен" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - level coolant response successfull" + Style.RESET_ALL)
        elif "Уровень охлаждающей жидкости увеличен" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - level coolant response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Проверка команды emergency_cooling
        connection.sendline("emergency_cooling".encode('utf-8'))
        response = connection.recvuntil("> ".encode('utf-8'), timeout=5)
        if "Экстренная система охлаждения активирована!" in response.decode('utf-8'):
            print(Fore.GREEN + f"[+] Checker 4 (Nuclear): {ip}:{port} - emergency_cooling response successfull" + Style.RESET_ALL)
        elif "Экстренная система охлаждения активирована!" not in response.decode('utf-8'):
            print(Fore.RED + f"[-] Checker 4 (Nuclear): {ip}:{port} - emergency_cooling response failed" + Style.RESET_ALL)
            connection.close()
            return 104, None

        # Закрытие соединения
        connection.close()
        return 101, None  # OK: Все команды успешно выполнены
    except:
        return 104, None   # NO: Ошибка входных данных


async def pwn(HOST):
    VERDICT = await check_reactor_commands(HOST, 9000)
    print(VERDICT)
    return VERDICT


loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost'))
