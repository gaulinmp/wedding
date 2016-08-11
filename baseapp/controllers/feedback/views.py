# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, request, flash,
                   session, redirect, url_for)
from flask_login import login_user, login_required, logout_user, current_user

from .forms import FeedbackForm
from .models import Feedback
from ..user.models import User
from ...utilities import flash_errors
from ...extensions import login_manager

blueprint = Blueprint('feedback', __name__, url_prefix='/feedback',
                      static_folder='../static',
                      template_folder='templates')

################################################################################
####           Routes                                                       ####
################################################################################

@blueprint.route("/", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm(request.form)
    msgs = (Feedback.query.join(User, Feedback.email==User.email)
                    .add_columns(User.first_name, User.last_name,
                                 *Feedback.__table__.columns)
                    .filter(Feedback.message_type != 'private')
                    .order_by(Feedback.created_at.desc())
            )
    return render_template("feedback/feedback.html", messages=msgs, form=form)

@blueprint.route("/secretsecret", methods=["GET",])
def secret():
    form = FeedbackForm(request.form)
    msgs = (Feedback.query.join(User, Feedback.email==User.email)
                    .add_columns(User.first_name, User.last_name,
                                 *Feedback.__table__.columns)
                    .filter(Feedback.message_type != 'song')
                    .order_by(Feedback.created_at.desc())
            )
    return render_template("feedback/feedback.html", messages=msgs, form=form)

@blueprint.route('/submit', methods=['GET', 'POST'])
def submit():
    form = FeedbackForm(request.form)
    if form.validate_on_submit():
        Feedback.create(email=current_user.email,
                        message_type=form.message_type.data,
                        message_string=form.message_string.data)
        flash('Thanks for Posting!', 'success')
        return redirect(url_for('feedback.feedback'))
    else:
        flash_errors(form)
    return render_template('feedback/feedback.html', form=form)

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
    ("Feedback", 'feedback.feedback'),
    ])
# Tack it on to blueprint for easy access in app's __init__.py
blueprint.extra_init = extra_init
