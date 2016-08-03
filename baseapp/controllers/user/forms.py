# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import request, url_for, redirect, session, current_app
from flask_wtf import Form
from wtforms import TextField, HiddenField
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
    first_name = TextField('First Name', [DataRequired()])
    last_name = TextField('Last Name', [DataRequired()])
    email = TextField('Email', [DataRequired()])
    question = TextField('Enter the bride\'s name', [DataRequired()])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.search(email=self.email.data)
        if user:
            self.email.errors.append("Email already registered. Please log in.")
            return False
        user = User.search(first_name=self.first_name.data, last_name=self.last_name.data)
        if user:
            self.first_name.errors.append("Name already registered. Please log in.")
            return False
        if 'lacey' not in '{}'.format(self.question.data).lower():
            self.question.errors.append("That's not the bride's name. Her name is Lacey. Try that instead.")
            return False
        return True


class LoginForm(RedirectForm):
    email = TextField('Email', [DataRequired()])
    question = TextField('Enter the bride\'s first name', [DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.search(email=self.email.data)
        if not self.user:
            self.email.errors.append('Unknown email. Please Register.')
            return False

        if 'lacey' not in '{}'.format(self.question.data).lower():
            self.question.errors.append("That's not the bride's name. Her name is Lacey. Try that instead.")
            return False

        return True


class ForgotForm(RedirectForm):
    first_name = TextField('First Name', [DataRequired()])
    last_name = TextField('Last Name', [DataRequired()])
