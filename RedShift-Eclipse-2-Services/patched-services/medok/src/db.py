import pymysql
import hashlib
from datetime import datetime, timedelta
from flask import current_app
from tenacity import retry, stop_after_attempt, wait_fixed

def get_db_connection():
    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_NAME']
    )

def create_table_if_not_exists(cursor, table_name, create_sql):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    if not cursor.fetchone():
        cursor.execute(create_sql)

def insert_admin_if_not_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """, ('admin', 'admin@localhost', hashlib.sha256('adminpassword'.encode()).hexdigest()))

def insert_doctors_if_not_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] == 0:
        doctors = [
            ('Иванов Иван Иванович', 'Терапевт', '/img/doctors/ivanov.png', '+7-999-123-4567', 'ivanov@example.com'),
            ('Петров Петр Петрович', 'Хирург', '/img/doctors/petrov.jpg', '+7-999-234-5678', 'petrov@example.com'),
            ('Сидорова Анна Сергеевна', 'Кардиолог', '/img/doctors/sidorova.webp', '+7-999-345-6789', 'sidorova@example.com'),
            ('Кузнецова Мария Ивановна', 'Невролог', '/img/doctors/kuznetsova.jpg', '+7-999-456-7890', 'kuznetsova@example.com'),
            ('Федоров Федор Федорович', 'Офтальмолог', '/img/doctors/fedorov.jpg', '+7-999-567-8901', 'fedorov@example.com'),
            ('Алексеева Ольга Дмитриевна', 'Педиатр', '/img/doctors/alekseeva.jpg', '+7-999-678-9012', 'alekseeva@example.com'),
            ('Смирнов Алексей Николаевич', 'Гинеколог', '/img/doctors/smirnov.jpg', '+7-999-789-0123', 'smirnov@example.com'),
            ('Морозов Дмитрий Андреевич', 'Дерматолог', '/img/doctors/morozov.jpg', '+7-999-890-1234', 'morozov@example.com'),
            ('Васильева Елена Петровна', 'Эндокринолог', '/img/doctors/vasilyeva.webp', '+7-999-901-2345', 'vasilieva@example.com'),
            ('Захаров Николай Павлович', 'Уролог', '/img/doctors/zakharov.jpg', '+7-999-012-3456', 'zakharov@example.com')
        ]
        
        insert_sql = """
            INSERT INTO doctors (full_name, specialization, image_path, phone_number, email)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_sql, doctors)

def insert_appointment_if_not_exists(cursor, user_id, doctor_id):
    cursor.execute("""
        SELECT COUNT(*) FROM appointments WHERE user_id = %s AND doctor_id = %s
    """, (user_id, doctor_id))
    
    if cursor.fetchone()[0] == 0:
        phone_number = '+7-999-000-1111'
        comment = 'Запись на консультацию по поводу здоровья.'
        appointment_datetime = datetime.now() + timedelta(days=5)
        
        cursor.execute("""
            INSERT INTO appointments (user_id, phone_number, doctor_id, datetime, comment)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, phone_number, doctor_id, appointment_datetime, comment))

@retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
def create_db_if_not_exists():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW DATABASES LIKE '{current_app.config['DB_NAME']}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {current_app.config['DB_NAME']}")

        cursor.execute(f"USE {current_app.config['DB_NAME']}")

        create_table_if_not_exists(cursor, 'users', """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        insert_admin_if_not_exists(cursor)

        create_table_if_not_exists(cursor, 'doctors', """
            CREATE TABLE doctors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                specialization VARCHAR(255) NOT NULL,
                image_path VARCHAR(255),
                phone_number VARCHAR(20),
                email VARCHAR(255)
            )
        """)
        
        insert_doctors_if_not_exists(cursor)

        create_table_if_not_exists(cursor, 'appointments', """
            CREATE TABLE appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                doctor_id INT NOT NULL,
                datetime DATETIME NOT NULL,
                comment TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        """)
        
        insert_appointment_if_not_exists(cursor, 1, 1)

        connection.commit()

    connection.close()
