import cherrypy
from flask import Flask, request
from paste.translogger import TransLogger

from exception import ValidationError
from message import Updates


def auth(Verify_Token, debug=True):
    app = Flask(__name__)
    app.debug = debug

    @app.route('/', methods=['GET'])
    def auth():
        if request.args.get('hub.verify_token') == Verify_Token:
            return request.args.get('hub.challenge'), 200
        else:
            raise ValidationError("Failed validation. Make sure the validation tokens match.")

    return app


def app_Run(main_func, debug=True):
    app = Flask(__name__)
    app.debug = debug
    @app.route('/', methods=['POST'])
    def hook():
        header = request.headers
        print(header)
        callback = request.get_json()
        web = Updates(callback)
        for message in web:
            main_func(message)
        return 'success', 200

    return app


def startServer(main_func=None, Verify_Token=None, debug=True, host="127.0.0.1", port="5000"):
    if main_func is None and Verify_Token is not None:
        app = auth(Verify_Token, debug)
    elif main_func is not None:
        app = app_Run(main_func, debug)
    else:
        raise Exception
    app_logged = TransLogger(app)
    cherrypy.tree.graft(app_logged, '/')
    cherrypy.config.update({
        'engine.autoreload_on': True,
        'log.screen': True,
        'server.socket_port': port,
        'server.socket_host': '0.0.0.0'
    })
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
