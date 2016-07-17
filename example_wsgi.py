#!/home1/USERNAME/python/2.7/bin/python
# ^^ This is a custom install of python, change it to reflect your server ^^

# put this file in public_html root, like ~/public_html/flask/huzzah
# below, set APPLICATION_ROOT to this file, including filename (here ``huzzah``)

import os
import sys
# Add the path where you checked out this repo, below it's ``flask_mold``
sys.path.insert(0, '/home1/USERNAME/projects/flask_mold/')
# You can add environmental variables here. Just don't check them in to your repo.
os.environ['SECRET_KEY'] = 'make me super secret yo'

from flup.server.fcgi import WSGIServer

# Change this line to run if 'baseapp' isn't the folder you're using.
from baseapp import create_app

# Because this is production, load the ProdConfig. Change to DevConfig for development.
from config.default_server import ProdConfig as config

config.APPLICATION_ROOT = '/flask/huzzah/' # <-- set this to this file path (see above)

app = create_app(config)

if __name__ == '__main__':
    WSGIServer(app).run()
