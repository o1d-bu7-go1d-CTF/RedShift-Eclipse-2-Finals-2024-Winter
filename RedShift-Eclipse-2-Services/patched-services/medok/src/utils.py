import os
import random
import hashlib
import pymysql
from .db import get_db_connection

def get_user_from_db(user_id):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    connection.close()
    return user

def get_tickets(email):
    email_hash = hashlib.md5(email.encode()).hexdigest()
    ticket_dir = f'src/static/tickets/{email_hash}'
    tickets = [
        {'name': file, 'path': f'tickets/{email_hash}/{file}'}
        for file in os.listdir(ticket_dir)
    ] if os.path.exists(ticket_dir) else []
    return tickets

def register_user(name, email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (name, email, password_hash))
        connection.commit()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    connection.close()
    return user

def validate_login(email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    connection.close()
    return user if user and user['password'] == password_hash else None

def get_doctors_from_db(search_query=None):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        if search_query:
            # Безопасная передача переменной в SQL-запрос
            query = f"""
                SELECT * FROM doctors
                WHERE LOWER(full_name) LIKE %s
            """
            cursor.execute(query, (f"%{search_query.lower()}%",))
        else:
            cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
    connection.close()
    return doctors

def create_ticket(email, name, phone, message):
    email_hash = hashlib.md5(email.encode()).hexdigest()
    ticket_dir = f'src/static/tickets/{email_hash}'

    if not os.path.exists(ticket_dir):
        os.makedirs(ticket_dir)

    ticket_number = random.randint(10000, 99999)
    ticket_filename = f'{ticket_dir}/ticket_{ticket_number}.txt'

    # Отказ от os.system() в пользу open() для предотвращения RCE
    ticket_content = (
        f"Заявка №{ticket_number}\n\n"
        f"Ваше имя: {name}\n\n"
        f"Ваш номер телефона: {phone}\n\n"
        f"Оставленное сообщение: {message}"
    )

    with open(ticket_filename, 'w', encoding='utf-8') as ticket_file:
        ticket_file.write(ticket_content)

def get_user_data(user_id):
    user = get_user_from_db(user_id)
    if user:
        tickets = get_tickets(user['email'])
        appointments = get_appointments(user_id)
        return user, tickets, appointments
    return None, None, None

def check_conflicting_appointment(doctor_id, appointment_datetime):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        query = """
            SELECT datetime FROM appointments
            WHERE doctor_id = %s AND
            ABS(TIMESTAMPDIFF(MINUTE, datetime, %s)) <= 15
        """
        cursor.execute(query, (doctor_id, appointment_datetime))
        return cursor.fetchone()
    connection.close()

def insert_appointment(user_id, phone, doctor_id, appointment_datetime, message):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        insert_query = """
            INSERT INTO appointments (user_id, phone_number, doctor_id, datetime, comment)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, phone, doctor_id, appointment_datetime, message))
        connection.commit()
    connection.close()

def get_appointments(user_id):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT a.id, a.datetime, d.specialization
            FROM appointments AS a
            JOIN doctors AS d ON a.doctor_id = d.id
            WHERE a.user_id = %s
        """, (user_id,))
        appointments = cursor.fetchall()
    connection.close()
    return appointments

def get_appointment_details(user_id, appointment_id):
    connection = get_db_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT a.id, a.datetime, d.full_name AS doctor_name, d.specialization
            FROM appointments AS a
            JOIN doctors AS d ON a.doctor_id = d.id
            WHERE a.user_id = %s AND a.id = %s
        """, (user_id, appointment_id))
        appointment = cursor.fetchone()
    connection.close()
    return appointment
