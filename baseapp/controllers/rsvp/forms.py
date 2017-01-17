# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import request, url_for, redirect, session, current_app

from flask_wtf import Form
from wtforms import TextField, SelectField, HiddenField, IntegerField
from wtforms.widgets import TextArea
from wtforms import validators
# from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.csrf.session import SessionCSRF

from .models import RSVP
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

class RSVPForm(RedirectForm):
    rsvp_name = TextField('Name', validators=[validators.DataRequired(),])
    rsvp_email = TextField('Email (optional)')

    rsvp_answer = SelectField('RSVP Answer',choices=[
        ('yes', 'I will be coming :)'),
        ('no', 'I won\'t be coming :('),
        ], validators=[validators.DataRequired(),])

    rsvp_number = IntegerField('Total Number Attending',
        validators=[validators.optional()]
        )

    rsvp_text = TextField('Message', widget=TextArea())

    def __init__(self, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(RSVPForm, self).validate()
        if not initial_validation:
            return False
        return True
