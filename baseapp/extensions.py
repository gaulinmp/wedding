# -*- coding: utf-8 -*-
"""
Extensions module.

create_app iterates through all_extensions array and calls init_app on each.
"""

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_login import LoginManager
login_manager = LoginManager()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# from flask_migrate import Migrate
# migrate = Migrate()

# from flask_cache import Cache
# cache = Cache()

# from flask_debugtoolbar import DebugToolbarExtension
# debug_toolbar = DebugToolbarExtension()

all_extensions = [bcrypt, login_manager, db]
