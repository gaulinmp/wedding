# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, request, flash,
                   session, redirect, url_for)
from flask_login import login_user, login_required, logout_user, current_user

from .forms import RSVPForm
from .models import RSVP
from ..user.models import User
from ...utilities import flash_errors
from ...extensions import login_manager

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
    rsps = (RSVP.query.join(User, RSVP.rsvp_email==User.email)
                    .add_columns(User.first_name, User.last_name,
                                 *RSVP.__table__.columns)
                    .order_by(RSVP.created_at.desc())
            )
    return render_template("rsvp/rsvp.html", rsvps=rsps, form=form)

@blueprint.route('/submit', methods=['GET', 'POST'])
def submit():
    form = RSVPForm(request.form)
    if form.validate_on_submit():
        RSVP.create(rsvp_email=form.rsvp_email.data or current_user.email,
                    rsvp_name=form.rsvp_name.data,
                    rsvp_answer=form.rsvp_answer.data,
                    rsvp_number=form.rsvp_number.data,
                    rsvp_text=form.rsvp_text.data)
        flash('Thanks for RSVPing!', 'success')
        return redirect(url_for('rsvp.rsvp'))
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
