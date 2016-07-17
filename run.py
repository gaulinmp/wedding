#!env python

from baseapp import create_app

from config.default_server import DevConfig

app = create_app(DevConfig)

if __name__ == '__main__':
    app.run()
