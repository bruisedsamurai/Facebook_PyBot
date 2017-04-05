import hmac
import logging
import queue
import threading
try:
    import ujson as json
except:
    import json

import cherrypy
from flask import Flask, request
from paste.translogger import TransLogger

from .exception import ValidationError
from .message import Updates

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run(main_func=None, Verify_Token=None, debug=True, app_secret_key=None):
    """
    Flask app runs in this function.
    Whenever a get request is received a the verify token is verified.
    And for a post request the request is verified and then data is passed to main_func.
    
    :param main_func: The function to which data is to be passed and is the code of the bot
    :param Verify_Token: needed for initial verification
    :param debug: 
    :param app_secret_key: app secret key needed for verify authenticity of the post request
    :return: flask app
    
    """
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
        logger.info(header)
        data = request.get_data()
        logger.info(data)
        callback = json.loads(data)
        logger.info(callback)
        if app_secret_key is not None:
            verify_result = verify(data, header, app_secret_key)
        else:
            verify_result = True
        if verify_result:
            Queue = queue.Queue()
            web = Updates(callback)
            for message in web:
                Queue.put(main_func(message))
                threading.Thread(target=Queue.get()).start()
        return "success", 200

    return app


def verify(callback, header, app_secret_key):
    """
    This function will verify the integrity and authenticity of the callback received
    
    :param callback: callback received from facebook
    :param header: headers of the request
    :param app_secret_key: facebook app secret key. You can find it on your app page
    :return: True if signature matches else returns false
    
    """
    X_hub_sign = header["X-Hub-Signature"]
    logger.info(X_hub_sign)
    method, sign = X_hub_sign.split("=")
    """
    Now a key will be created of callback using app secret as the key.
    And compared with xsignature found in the the headers of the request.
    If both the keys match then the function will run further otherwise it will halt
    """
    hmac_object = hmac.new(app_secret_key.encode("utf-8"), callback, "sha1")
    key = hmac_object.hexdigest()
    logger.info(key)
    return hmac.compare_digest(sign, key)


def startServer(main_func=None, Verify_Token=None, debug=True, host="127.0.0.1", port="5000", app_secret_key=None):
    if main_func is not None and Verify_Token is not None:
        app = run(main_func, Verify_Token, debug, app_secret_key)
    elif Verify_Token is not None:
        app = run(Verify_Token=Verify_Token, debug=debug, app_secret_key=app_secret_key)
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
