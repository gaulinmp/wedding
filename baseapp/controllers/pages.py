# -*- coding: utf-8 -*-
from flask import render_template, Blueprint

blueprint = Blueprint('baseapp', __name__,
                      static_folder='../static',
                      template_folder='../templates')

################################################################################
####           Routes                                                       ####
################################################################################

@blueprint.route('/')
def home():
    return render_template('pages/home.html')

@blueprint.route('/about')
def about():
    return render_template('pages/about.html')

@blueprint.route('/deets')
def deets():
    return render_template('pages/deets.html')

@blueprint.route('/accommodations')
def accommodations():
    return render_template('pages/accommodations.html')

@blueprint.route('/gifts')
def gifts():
    return render_template('pages/gifts.html')

# Add more routes here. Or copy this file and make a new blueprint.

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
    ("About Us", 'baseapp.about'),
    ("Wedding", 'baseapp.deets'),
    ("Accomodations", 'baseapp.accommodations'),
    ("Registry", 'baseapp.gifts'),
    ])
# Tack it on to blueprint for easy access in app's __init__.py
blueprint.extra_init = extra_init
