# -*- coding: utf-8 -*-
from sqlalchemy.sql import func

from flask import (Blueprint, render_template, request, flash,
                   session, redirect, url_for)

from .forms import RSVPForm
from .models import RSVP
from ...utilities import flash_errors
# from ...extensions import login_manager

blueprint = Blueprint('rsvp', __name__, url_prefix='/rsvp',
                      static_folder='../static',
                      template_folder='templates')

################################################################################
####           Routes                                                       ####
################################################################################

@blueprint.route("/", methods=["GET", "POST"])
def rsvp():
    form = RSVPForm(request.form)
    return render_template("rsvp/rsvp.html", form=form)

@blueprint.route("/secretsecret", methods=["GET",])
def secret():
    form = RSVPForm(request.form)
    rsps = (RSVP.query.order_by(RSVP.created_at.desc()))
    tot_num = (RSVP.query
                   .filter_by(rsvp_answer="yes")
                   .with_entities(func.sum(RSVP.rsvp_number).label('tot'))
                   .first())[0]
    return render_template("rsvp/rsvp.html", rsvps=rsps, form=form,
                           guestlist=True, tot_num=tot_num)

@blueprint.route('/submit', methods=['GET', 'POST'])
def submit():
    form = RSVPForm(request.form)
    if form.validate_on_submit():
        RSVP.create(rsvp_email=form.rsvp_email.data,
                    rsvp_name=form.rsvp_name.data,
                    rsvp_answer=form.rsvp_answer.data,
                    rsvp_number=form.rsvp_number.data,
                    rsvp_text=form.rsvp_text.data)
        if form.rsvp_answer.data == "yes":
            flash('Thanks for RSVPing! We look forward to seeing you in April!',
                  'success')
        else:
            flash('Thanks for RSVPing! We\'re sorry you can\'t make it. You will be missed!',
                  'success')
        return redirect(url_for('baseapp.home'))
    else:
        flash_errors(form)
    return render_template('rsvp/rsvp.html', form=form)

################################################################################
####           Add to App Context Manager                                   ####
################################################################################
def extra_init(app):
    """Extra blueprint initialization that requires application context."""
    if 'header_links' not in app.jinja_env.globals:
        app.jinja_env.globals['header_links'] = []
    # Add links to 'header_links' var in jinja globals. This allows header_links
    # to be read by all templates in the app instead of just this blueprint.
    app.jinja_env.globals['header_links'].extend([
    ("RSVP", 'rsvp.rsvp'),
    ])
# Tack it on to blueprint for easy access in app's __init__.py
blueprint.extra_init = extra_init
