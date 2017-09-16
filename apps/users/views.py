# -*- coding: utf-8 -*-

import json
import random

from models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import MyUserForm, RestorePassword
from ..basic.wrappers import required_fields, form_valid, resp_json
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
from validators import RESTORE_CODE_MIN_VALUE, RESTORE_CODE_MAX_VALUE


@resp_json
@required_fields('MyUser', ['username', 'password', 'repeat_password', 'first_name', 'last_name', 'email', 'phone'])
@form_valid(MyUserForm)
def signup_ctrl(request):
    data = json.loads(request.body).get('data-MyUser')

    user_exist = MyUser.objects.\
        filter(Q(username=data.get('username')) | Q(email=data.get('email')))
    rep_pass = data.pop('repeat_password')
    if not user_exist and rep_pass and rep_pass == data.get('password', ''):
        username, password, email = data.pop('username'), data.pop('password'), data.pop('email')
        user = MyUser.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        for key, f_value in data.items():
            setattr(user, key, f_value)
        user.save()
        return {'error': '', 'data': [], 'result': True}
    return {'error': 'invalid_signup', 'data': ['username'], 'result': False}


@resp_json
@required_fields('MyUser', ['username', 'password'])
@form_valid(MyUserForm)
def login_ctrl(request):
    data = json.loads(request.body).get('data-MyUser')
    user = authenticate(username=data.get('username'), password=data.get('password'))
    if user:
        login(request=request, user=user)
        session_expiry = 60 * 60 * 24 * 30 if data.get('remember') else 60 * 60 * 5
        request.session.set_expiry(session_expiry)
        return {'error': '', 'data': [], 'result': True}
    return {'error': 'invalid_login', 'data': ['username', 'password'], 'result': False}

@resp_json
@login_required
def logout_ctrl(request):
    logout(request)
    return {'error': '', 'data': [], 'result': True}

@resp_json
@required_fields('MyUser', ['email'])
def forgot_ctrl(request):
    data = json.loads(request.body).get('data-MyUser')
    email = data.get('email')
    user = MyUser.objects.filter(email=email)
    if user:
        number = random.randint(RESTORE_CODE_MIN_VALUE, RESTORE_CODE_MAX_VALUE)
        request.session['forgot'] = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%s'),
            'number': number,
        }
        send_mail(
            subject='Відновлення паролю',
            message="""Для відновлення паролю введіть цифри на сайті:
            %s
            
            Далі введіть новий пароль
            
            Посилання активне протягом 10 хвилин
            
            !!!Якщо ви не намагались змінити пароль, то проігноруйте це повідомлення
            """ % (number),
            from_email='orders.com.ua@gmail.com',
            recipient_list=[email]
        )
        return {'error': '', 'data': [], 'result': True}

    else:
        return {'error': 'user_not_found', 'data': ['email'], 'result': False}

@form_valid(RestorePassword, True)
def restore_pass_ctrl(request):
    pass