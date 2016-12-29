# -*- coding: utf-8 -*-
"""
Handles all RSVP interaction.

Could have a database backend, or plaintext.
"""
import os
import json
import datetime as dt

from flask import current_app

# from baseapp.extensions import bcrypt
from baseapp.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)

class RSVP(SurrogatePK, Model):
    __tablename__ = 'rsvp'
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    rsvp_name = Column(db.String(80), unique=False, nullable=False)
    rsvp_email = Column(db.String(80), unique=False, nullable=True)
    rsvp_answer = Column(db.String(16), unique=False, nullable=False)
    rsvp_number = Column(db.Integer(), unique=False, nullable=True)
    rsvp_text = Column(db.Text(length=1024**2), nullable=True)

    def __repr__(self):
        return '<RSVP({}:{})>'.format(self.id, self.rsvp_email)

    @staticmethod
    def get_by_id(rsvp_id):
        return search(rsvp_id=rsvp_id)

    @staticmethod
    def search(rsvp_id=None, rsvp_email=None, rsvp_answer=None):
        """Searches USER database, returns RSVP object in search order:
        ID > rsvp_email
        """
        if rsvp_id is not None:
            return RSVP.query.filter_by(id=rsvp_id).first()
        if rsvp_email is not None:
            return RSVP.query.filter_by(rsvp_email=rsvp_email).first()
        if rsvp_answer is not None:
            return RSVP.query.filter_by(rsvp_answer=rsvp_answer)
        return None

    @staticmethod
    def create(**kwargs):
        """Factory method wrapping RSVP(**kwargs)."""
        if ('rsvp_answer' not in kwargs or
            'rsvp_number' not in kwargs):
            print("Email: {}\tName: {}\tAnswer: {}"
                  .format(kwargs.get('rsvp_email', None),
                          kwargs.get('rsvp_name', None),
                          kwargs.get('rsvp_answer', None)))
            return None
        msg = RSVP(rsvp_name=kwargs.pop('rsvp_name', None),
                   rsvp_answer=kwargs.pop('rsvp_answer', None),
                   rsvp_email=kwargs.pop('rsvp_email', None),
                   rsvp_number=kwargs.pop('rsvp_number', None),
                   rsvp_text=kwargs.pop('rsvp_text', None),
                   **kwargs)
        msg.save()
        return msg
