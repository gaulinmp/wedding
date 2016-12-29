# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import request, url_for, redirect, session, current_app

from flask_wtf import Form
from wtforms import TextField, SelectField, HiddenField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.csrf.session import SessionCSRF

from .models import Feedback
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

class FeedbackForm(RedirectForm):
    name = TextField('Name', validators=[DataRequired(),])
    message_type = SelectField('Message Type',choices=[
        ('private', 'Private Message to the Couple'),
        ('public', 'Public Message'),
        ('song', 'Song Suggestion'),
        ])
    message_string = TextField(
        'Message', validators=[DataRequired(),], widget=TextArea()
        )

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.user = None

    # def validate(self):
    #     initial_validation = super(FeedbackForm, self).validate()
    #     if not initial_validation:
    #         return False
    #     try:
    #         if not current_user.email:
    #             self.email.errors.append("No valid user found. Please log in.")
    #             return False
    #     except AttributeError:
    #         self.email.errors.append("No valid user found. Please log in.")
    #         return False
    #     if not current_user.is_authenticated:
    #         self.email.errors.append("No valid user found. Please log in.")
    #         return False
    #     return True
