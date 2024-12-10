from flask import Blueprint, render_template, render_template_string, request, redirect, url_for, session
from .utils import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return render_template('auth.html')

    user, tickets, appointments = get_user_data(user_id)
    if not user:
        return render_template('auth.html')

    return render_template('profile.html', 
                           name=session.get('name', user['username']), 
                           email=user['email'], 
                           tickets=tickets, 
                           appointments=appointments,
                           user_id=user_id)

@main.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = register_user(name, email, password)
    if not user:
        return redirect(url_for('main.profile', error="Ошибка регистрации"))

    session['user_id'] = user['id']
    session['name'] = name

    # Безопасный редирект в профиль
    return redirect(url_for('main.profile'))

@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = validate_login(email, password)
    if not user:
        return redirect(url_for('main.profile', error="Неверный e-mail или пароль!"))

    session['user_id'] = user['id']
    session['name'] = user['username']
    return redirect(url_for('main.profile'))

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    return redirect(url_for('main.index'))

@main.route('/doctors')
def doctors():
    if 'user_id' not in session:
        return render_template('auth.html')

    search_query = request.args.get('search', '')
    doctors_list = get_doctors_from_db(search_query)
    return render_template('doctors.html', doctors=doctors_list)

@main.route('/services')
def services():
    if 'user_id' not in session:
        return render_template('auth.html')
    return render_template('services.html', name=session['name'])

@main.route('/ticket', methods=['POST'])
def ticket():
    user_id = session.get('user_id')
    if not user_id:
        return render_template('auth.html')

    user = get_user_from_db(user_id)
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')

    create_ticket(user['email'], name, phone, message)
    return render_template('ticket.html')

@main.route('/appointment')
def appointment():
    if 'user_id' not in session:
        return render_template('auth.html')

    doctor_id = request.args.get('doctor_id')
    doctors_list = get_doctors_from_db()
    selected_doctor = next((d for d in doctors_list if str(d['id']) == doctor_id), None)

    return render_template('appointment.html', name=session['name'], doctors_list=doctors_list, selected_doctor=selected_doctor)

@main.route('/process_appointment', methods=['POST'])
def process_appointment():
    user_id = session.get('user_id')

    phone = request.form.get('phone')
    doctor_id = request.form.get('doctor')
    date = request.form.get('date')
    time = request.form.get('time')
    message = request.form.get('message', '')

    appointment_datetime = f"{date} {time}:00"
    
    conflicting_appointment = check_conflicting_appointment(doctor_id, appointment_datetime)
    if conflicting_appointment:
        conflicting_time = conflicting_appointment['datetime'].strftime('%H:%M')
        return render_template('result.html', 
                               message=f"Прием длится 15 минут. Уже зарегистрирована запись на {conflicting_time}, попробуйте записаться на другое время.")

    insert_appointment(user_id, phone, doctor_id, appointment_datetime, message)

    return render_template('result.html', 
                           message="Успешная запись на прием. Отслеживайте свои записи в личном кабинете.")

@main.route('/view_appointment/<int:user_id>/<int:appointment_id>')
def view_appointment(user_id, appointment_id):
    appointment = get_appointment_details(user_id, appointment_id)

    # Проверка user_id сессии; отсутствие вывода, если user_id не совпал
    if session.get('user_id') != user_id: appointment = None
    return render_template('view_appointment.html', appointment=appointment)