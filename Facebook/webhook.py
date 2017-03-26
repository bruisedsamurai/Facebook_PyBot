import cherrypy
from flask import Flask, request
from paste.translogger import TransLogger

from exception import ValidationError
from message import Updates
try:
    import ujson as json
except:
    import json

import hmac


def run(main_func=None, Verify_Token=None, debug=True,app_secret_key=None):
    app = Flask(__name__)
    app.debug = debug

    @app.route('/', methods=['GET'])
    def auth():
        if request.args.get('hub.verify_token') == Verify_Token:
            return request.args.get('hub.challenge'), 200
        else:
            raise ValidationError("Failed validation. Make sure the validation tokens match.")

    @app.route('/', methods=['POST'])
    def hook():
        header = request.headers
        callback = request.get_json()
        if app_secret_key is not None:
            verify_result=verify(callback,header,app_secret_key)
        else:
            verify_result=True
        if verify_result:
            web = Updates(callback)
            for message in web:
                main_func(message)
            return "success", 200
        else:
            return "Die Please"

    return app

def verify(callback,header,app_secret_key):
    try:
        keyback=json.dumps(callback)
        X_hub_sign=header["X-Hub-Signature"]
        method,sign=X_hub_sign.split("=")
    except:
        pass
    """
    Now a key will be created of callback using app secret as the key.
    And compared with xsignature found in the the headers of the request.
    If both the keys match then the function will run further otherwise it will halt
    """
    hmac_object=hmac.new(app_secret_key.encode("utf-8"),str(keyback).encode("utf-8"),"sha1")
    key=hmac_object.hexdigest()
    if sign==key:
        return True
    else:
        return False


def startServer(main_func=None, Verify_Token=None, debug=True, host="127.0.0.1", port="5000",app_secret_key=None):
    if main_func is not None and Verify_Token is not None:
        app = run(main_func, Verify_Token, debug,app_secret_key)
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
