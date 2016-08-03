# -*- coding: utf-8 -*-
"""
Handles all Feedback interaction.

Could have a database backend, or plaintext.
"""
import os
import json
import datetime as dt

from flask import current_app

from baseapp.extensions import bcrypt
from baseapp.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)

class Feedback(SurrogatePK, Model):
    __tablename__ = 'feedback'
    email = Column(db.String(80), unique=False, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    message_type = Column(db.String(16), nullable=False)
    message_string = Column(db.Text(length=1024**2), nullable=False)

    def __repr__(self):
        return '<Feedback({}:{})>'.format(self.id, self.email)

    @staticmethod
    def get_by_id(feedback_id):
        return search(feedback_id=feedback_id)

    @staticmethod
    def search(feedback_id=None, email=None, message_type=None):
        """Searches USER database, returns Feedback object in search order:
        ID > email
        """
        if feedback_id is not None:
            return Feedback.query.filter_by(id=feedback_id).first()
        if email is not None:
            return Feedback.query.filter_by(email=email).first()
        if message_type is not None:
            return Feedback.query.filter_by(message_type=message_type)
        return None

    @staticmethod
    def create(**kwargs):
        """Factory method wrapping Feedback(**kwargs)."""
        if ('email' not in kwargs or
            'message_type' not in kwargs or
            'message_string' not in kwargs):
            print("Username: {}\tmessage: {}".format(kwargs.get('email', None),
                                                     kwargs.get('message_type', None),
                                                     kwargs.get('message_string', None)))
            return None
        msg = Feedback(email=kwargs.pop('email', None),
                       message_type=kwargs.pop('message_type', None),
                       message_string=kwargs.pop('message_string', None),
                       **kwargs)
        msg.save()
        return msg
