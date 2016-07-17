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

from baseapp.extensions import bcrypt
from baseapp.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)

class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'
    #user_id = Column(db.Integer, primary_key=True, nullable=False)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    admin = Column(db.Boolean(), default=False)
    authenticated = Column(db.Boolean(), default=False)

    # search = search
    # create = create

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        if not password:
            self.password = None
        else:
            self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        if value is None:
            return False
        return bcrypt.check_password_hash(self.password, value)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def is_active(self):
        """Method expected by Flask Login."""
        return self.active

    def is_authenticated(self):
        """Checks for loggedin-ness"""
        return self.authenticated

    def authenticate(self, is_authentic=False):
        """Sets loggedin-ness. VERY vulnerable to race conditions."""
        self.authenticated = is_authentic
        self.save()
        return self.authenticated

    def __repr__(self):
        return '<User({}:{})>'.format(self.id, self.username)

    @staticmethod
    def get_by_id(user_id):
        return search(user_id=user_id)

    @staticmethod
    def search(user_id=None, username=None, email=None):
        """Searches USER database, returns User object in search order:
        ID > username > email
        """
        if user_id is not None:
            return User.query.filter_by(id=user_id).first()
        if username is not None:
            return User.query.filter_by(username=username).first()
        if email is not None:
            return User.query.filter_by(email=email).first()
        return None

    @staticmethod
    def create(**kwargs):
        """Factory method wrapping User(**kwargs)."""
        if ('username' not in kwargs or
            'email' not in kwargs):
            return None
        if 'admin' in kwargs:
            kwargs.pop('admin')  # Admin is set manually.
        if 'active' in kwargs:
            active = kwargs.pop('active')
        active = False if 'password' in kwargs else active  # no password, no dice
        user = User(username=kwargs.pop('username', None),
                    email=kwargs.pop('email', None),
                    password=kwargs.pop('password', None),
                    active=active,
                    admin=False,  # Don't let admins be created. Set manually.
                    **kwargs)
        user.save()
        return user
