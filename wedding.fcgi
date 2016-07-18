#!/home1/mgaulinc/python/2.7/bin/python

import os
import sys
sys.path.insert(0, '/home1/mgaulinc/projects/python/wedding/')
os.environ['SECRET_KEY'] = 'fanu90faun9pmasfp9useunvs39oputhnsoeihnvw9348n'

import logging
from logging import Formatter
log = logging.getLogger()
h = logging.FileHandler("/home1/mgaulinc/public_html/files/werr.txt")
h.setFormatter(Formatter(
    '%(asctime)s\t%(levelname)s\t[%(pathname)s:%(lineno)d]\t%(message)s :: \t'
))
log.setLevel(logging.DEBUG)
h.setLevel(logging.DEBUG)
log.addHandler(h)
log.critical("Loading request for logs...")

from flup.server.fcgi import WSGIServer
from baseapp import create_app

from config.default_server import ProdConfig as config

class ScriptNameStripper(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)

app = ScriptNameStripper(create_app(config))

if __name__ == '__main__':
    WSGIServer(app).run()
