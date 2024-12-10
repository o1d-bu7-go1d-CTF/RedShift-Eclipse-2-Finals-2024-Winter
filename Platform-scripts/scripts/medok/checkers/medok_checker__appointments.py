# Checker (Appointments) for MedOK
# Author: boomgarang

import aiohttp
import asyncio
from colorama import Fore, Style
from bs4 import BeautifulSoup
from .medok_checker__helper import register_user, delete_user_from_db, delete_appointment

async def cleanup(message, email, HOST):
    await delete_appointment(message, HOST)
    await delete_user_from_db(email, HOST)

async def check_appointment(HOST, PORT):
    register_params = await register_user(HOST, PORT)
    if register_params[0] != 101:
        return register_params[0], None
    
    cookies, email = register_params[1]

    try:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            message = "Хотел бы уточнить детали."
            appointment_data = {
                "phone": "1234567890",
                "doctor": "1",
                "date": "2024-11-30",
                "time": "10:30",
                "message": message
            }
            async with session.post(f'http://{HOST}:{PORT}/process_appointment', data=appointment_data) as resp_appointment:
                if resp_appointment.status != 200:
                    print(Fore.RED + f"[-] Checker 1 (Medok): {HOST}:{PORT} - Appointment creation failed" + Style.RESET_ALL)
                    await cleanup(message, email, HOST)
                    return 104, None
                appointment_response = await resp_appointment.text()
                if "Успешная запись на прием" not in appointment_response:
                    print(Fore.RED + f"[-] Checker 1 (Medok): {HOST}:{PORT} - Appointment not confirmed" + Style.RESET_ALL)
                    await cleanup(message, email, HOST)
                    return 104, None

            async with session.get(f'http://{HOST}:{PORT}/profile') as resp_profile:
                if resp_profile.status != 200:
                    print(Fore.RED + f"[-] Checker 1 (Medok): {HOST}:{PORT} - Profile retrieval failed" + Style.RESET_ALL)
                    await cleanup(message, email, HOST)
                    return 104, None
                profile_html = await resp_profile.text()
                
                soup = BeautifulSoup(profile_html, 'html.parser')
                appointment_link = None
                for a_tag in soup.select('.appointments-list a'):
                    href = a_tag.get('href')
                    if '/view_appointment' in href:
                        appointment_link = href
                        break
                
                if not appointment_link:
                    print(Fore.RED + f"[-] Checker 1 (Medok): {HOST}:{PORT} - Appointment link not found" + Style.RESET_ALL)
                    await cleanup(message, email, HOST)
                    return 104, None

            async with session.get(f'http://{HOST}:{PORT}{appointment_link}') as resp_view:
                if resp_view.status != 200:
                    print(Fore.RED + f"[-] Checker 1 (Medok): {HOST}:{PORT} - Appointment view failed" + Style.RESET_ALL)
                    await cleanup(message, email, HOST)
                    return 104, None
                view_html = await resp_view.text()

                if "Иванов Иван Иванович" not in view_html:
                    print(Fore.RED + f"[-] Checker 1 (Medok): {HOST}:{PORT} - Appointment details mismatch" + Style.RESET_ALL)
                    await cleanup(message, email, HOST)
                    return 104, None

            await cleanup(message, email, HOST)

            print(Fore.GREEN + f"[+] Checker 1 (Medok): {HOST}:{PORT} - Appointment process successful" + Style.RESET_ALL)
            return 101, None

    except Exception as e:
        print(Fore.RED + f"[-] Checker 1 (Medok): {HOST}:{PORT} - An error occurred: {e}" + Style.RESET_ALL)
        await cleanup(message, email, HOST)
        return 104, None

async def pwn(HOST):
    VERDICT = await check_appointment(HOST, 5000)
    print(VERDICT)
    return VERDICT
