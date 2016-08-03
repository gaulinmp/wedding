# -*- coding: utf-8 -*-
"""
Handles all User interaction.

Could have a database backend, or plaintext.
"""
import os
import json
import datetime as dt

from flask import current_app
from flask_login import UserMixin

# from baseapp.extensions import bcrypt
from baseapp.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)

class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'
    email = Column(db.String(80), unique=True, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=False)
    last_name = Column(db.String(30), nullable=False)
    authenticated = Column(db.Boolean(), default=False)

    def __init__(self, email=None, first_name=None, last_name=None, **kwargs):
        db.Model.__init__(self, email=email, first_name=first_name,
                          last_name=last_name, **kwargs)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def is_active(self):
        """Method expected by Flask Login."""
        return True

    def is_authenticated(self):
        """Checks for loggedin-ness"""
        return self.authenticated

    def authenticate(self, is_authentic=False):
        """Sets loggedin-ness. VERY vulnerable to race conditions."""
        self.authenticated = is_authentic
        self.save()
        return self.authenticated

    def __repr__(self):
        return '<User({}:{})>'.format(self.id, self.email)

    @staticmethod
    def get_by_id(user_id):
        return search(user_id=user_id)

    @staticmethod
    def search(user_id=None, email=None, first_name=None, last_name=None):
        """Searches USER database, returns User object in search order:
        ID > username > email
        """
        if user_id is not None:
            return User.query.filter_by(id=user_id).first()
        if email is not None:
            return User.query.filter_by(email=email).first()
        if first_name is not None and last_name is not None:
            return User.query.filter_by(first_name=first_name,
                                        last_name=last_name).first()
        return None

    @staticmethod
    def create(**kwargs):
        """Factory method wrapping User(**kwargs)."""
        if ('email' not in kwargs or
            'first_name' not in kwargs or
            'last_name' not in kwargs):
            return None
        if 'question' in kwargs:
            _answer = kwargs.pop('question', None)
            if 'lacey' not in _answer:
                print("Found answer, but it was {}".format(_answer))
                return None
        if 'authenticated' in kwargs:
            _ = kwargs.pop('authenticated', None)
        user = User(email=kwargs.pop('email', None),
                    first_name=kwargs.pop('first_name', None),
                    last_name=kwargs.pop('last_name', None),
                    authenticated=False,
                    **kwargs)
        user.save()
        return user
