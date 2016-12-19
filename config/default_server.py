# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    SITE_NAME = "Lacey + Mac"
    SITE_AUTHOR = "Mac Gaulin"
    SITE_DESCRIPTION = "Wedding site for Lacey and Mac."
    SECRET_KEY = os_env.get('SECRET_KEY', 'wegongetmarried')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # config directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    USE_CDN = True


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DB_NAME = 'database.db'
    GOOGLE_ANALYTICS = 'UA-80889496-1'
    GOOGLE_RECAPTCHA = '6LfpIA8UAAAAANnfnhrUF84a2z7ui-tlZN2msV17'
    DBFILE_PATH = os.path.join(Config.APP_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + DBFILE_PATH)


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    USE_CDN = False
    UPLOAD_KEY = 'test'
    WTF_CSRF_ENABLED = False
    DB_NAME = 'dev.db'
    DBFILE_PATH = os.path.join(Config.APP_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + DBFILE_PATH)
    GOOGLE_RECAPTCHA = '6LfpIA8UAAAAANnfnhrUF84a2z7ui-tlZN2msV17'


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    USE_CDN = False
