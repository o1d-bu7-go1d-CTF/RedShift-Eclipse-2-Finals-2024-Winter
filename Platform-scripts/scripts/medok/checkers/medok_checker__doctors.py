# Checker (Doctors) for MedOK
# Author: boomgarang

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from colorama import Fore, Style
from .medok_checker__helper import register_user, delete_user_from_db

async def search_test(HOST, PORT, email, search_query, cookies, expected_count):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{HOST}:{PORT}/doctors', params={'search': search_query}, cookies=cookies) as resp:
                if resp.status == 200:
                    page = await resp.text()
                    soup = BeautifulSoup(page, 'html.parser')
                    doctors = soup.find_all(class_='doctor-card')
                    if len(doctors) == expected_count:
                        print(Fore.GREEN + f"[+] Checker 3 (Medok): {HOST}:{PORT} - Search query '{search_query}': Expected {expected_count} results, found {len(doctors)}." + Style.RESET_ALL)
                        return 101, None
                    else:
                        print(Fore.RED + f"[-] Checker 3 (Medok): {HOST}:{PORT} - Search query '{search_query}': Expected {expected_count} results, found {len(doctors)}." + Style.RESET_ALL)
                        await delete_user_from_db(email, HOST)
                        return 104, None
                else:
                    print(Fore.RED + f"[-] Checker 3 (Medok): {HOST}:{PORT} - Error during search query '{search_query}'" + Style.RESET_ALL)
                    await delete_user_from_db(email, HOST)
                    return 104, None
    except Exception as e:
        print(Fore.RED + f"[-] Checker 3 (Medok): {HOST}:{PORT} - An error occured: {e}" + Style.RESET_ALL)
        await delete_user_from_db(email, HOST)
        return 104, None

async def checker_doctors(HOST, PORT):
    register_params = await register_user(HOST, PORT)
    if register_params[0] != 101:
        return register_params[0], None
    cookies, email = register_params[1]

    empty_search = await search_test(HOST, PORT, email, '', cookies, 10)
    if empty_search[0] != 101:
        print(empty_search)
        return empty_search

    peters_search = await search_test(HOST, PORT, email, 'петров', cookies, 2)
    if peters_search[0] != 101:
        return peters_search

    ivan_search = await search_test(HOST, PORT, email, 'иван', cookies, 2)
    if ivan_search[0] != 101:
        return ivan_search

    fedor_search = await search_test(HOST, PORT, email, 'федор', cookies, 1)
    if fedor_search[0] != 101:
        return fedor_search

    delete_status = await delete_user_from_db(email, HOST)
    if delete_status[0] != 101:
        return delete_status
    
    return 101, None

async def pwn(HOST):
    VERDICT = await checker_doctors(HOST, 5000)
    print(VERDICT)
    return VERDICT
