# Checker (Services) for MedOK
# Author: boomgarang

import re
import aiohttp
import asyncio
from colorama import Fore, Style
from medok_checker__helper import register_user, delete_user_from_db

async def create_ticket(HOST, PORT, email, cookies):
    try:
        async with aiohttp.ClientSession(cookies=cookies) as client_session:
            ticket_data = {
                "name": email,
                "phone": "+1234567890",
                "message": "Test message from checker."
            }
            async with client_session.post(f'http://{HOST}:{PORT}/ticket', data=ticket_data) as resp:
                if resp.status in [200, 302]:
                    print(Fore.GREEN + "[+] Ticket created successfully" + Style.RESET_ALL)
                    return 101, None
                else:
                    print(Fore.RED + "[-] Ticket creation failed" + Style.RESET_ALL)
                    await delete_user_from_db(email)
                    return 104, None
    except Exception as e:
        print(Fore.RED + f"[-] An error occured: {e}" + Style.RESET_ALL)
        await delete_user_from_db(email)
        return 110, None

async def checker_tickets(HOST, PORT):
    register_params = await register_user(HOST, PORT)
    if register_params[0] != 101:
        return register_params[0], None
    cookies, email = register_params[1]
    create_ticket_status = await create_ticket(HOST, PORT, email, cookies)
    if create_ticket_status[0] != 101:
        return create_ticket_status
    try:
        async with aiohttp.ClientSession(cookies=cookies) as client_session:
                async with client_session.get(f'http://{HOST}:{PORT}/profile') as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        delete_status = await delete_user_from_db(email)
                        if delete_status[0] != 101:
                            return delete_status
                        if re.search(r'ticket_\d{5}\.txt', text):
                            print(Fore.GREEN + "[+] Tickets fetched successfully" + Style.RESET_ALL)
                            return 101, None
                print(Fore.RED + "[-] Failed to fetch tickets" + Style.RESET_ALL)
                await delete_user_from_db(email)
                return 104, None
    except Exception as e:
        print(Fore.RED + f"[-] An error occured: {e}" + Style.RESET_ALL)
        await delete_user_from_db(email)
        return 110, None

async def pwn(HOST):
    VERDICT = await checker_tickets(HOST, 5000)
    print(VERDICT)
    return VERDICT

loop = asyncio.get_event_loop()
loop.run_until_complete(pwn('localhost'))
