# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import request, url_for, redirect, session, current_app
from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.csrf.session import SessionCSRF

from .models import User
from ...utilities import get_redirect_target, is_safe_url

class RedirectForm(Form):
    nextpage = HiddenField()

    def __init__(self, *args, **kwargs):
        super(RedirectForm, self).__init__(*args, **kwargs)
        if not self.nextpage.data:
            self.nextpage.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.nextpage.data):
            return redirect(self.nextpage.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class RegisterForm(RedirectForm):
    username = TextField(
        'Username', validators=[DataRequired(), Length(min=1, max=31)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=1, max=64)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=1, max=64)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.search(username=self.username.data)
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.search(email=self.email.data)
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class LoginForm(RedirectForm):
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.search(username=self.username.data)
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False

        return True


class ForgotForm(RedirectForm):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=1, max=64)]
    )
