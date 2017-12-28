import hmac
import logging
import traceback
from threading import Thread

import falcon

try:
    import ujson as json
except ImportError:
    import json  # type: ignore

from .message import updates
from .handlers import text_handler, attachment_handler

logger = logging.getLogger(__name__)


def http(main_func=None, verify_token=None, app_secret_key=None):
    """
    Setups an interface for receiving requests from Facebook. It will handle the verification of webhook and also
    all requests send by Facebook

    :param main_func: one or a list of callable which should be called whenever a callback is received from Facebook.
    :param verify_token: verification token used to verify the webhook initially.
    :type verify_token: str
    :param app_secret_key: this key will be used to verify if every request received is authentic.
    :type app_secret_key: str
    :return: an wsgi app.
    """
    app = falcon.API()

    class HttpApi(object):

        def on_get(self, req, resp):
            if req.get_param("hub.verify_token") == verify_token:
                resp.status = falcon.HTTP_200
                resp.body = req.get_param('hub.challenge')
            else:
                resp.status = falcon.HTTP_200
                resp.body = "Failed validation. Make sure the validation tokens match."

        def on_post(self, req, resp):
            resp.status = falcon.HTTP_200
            resp.body = "success"
            signature = req.get_header("X-Hub-Signature")
            data = req.stream.read()
            verify_result = True  # verification of the callback is optional currently.
            # Therefore if no app secret key is passed then the bot will run anyway
            if app_secret_key is not None:
                verify_result = _verify(data, signature, app_secret_key)
            if verify_result:
                callback = json.loads(data)
                web = updates(callback)
                is_call = _check_callable_list(main_func)
                for message in web:  # Sometimes there are more than one number of callbacks.
                    if not is_call:
                        _run(main_func, message)
                    else:
                        for each_callable in main_func:
                            _run(each_callable, message)

    api = HttpApi()
    app.add_route('/', api)
    return app


def _check_callable_list(func):
    if callable(func):
        return False
    elif isinstance(func, list):
        for each_index in func:
            if not callable(each_index):
                return False
        return True


def _run(func, message):
    try:
        thread = Thread(target=func(message))
        thread.daemon = True
        thread.run()
    except:
        print(traceback.print_exc())


def _verify(callback, signature, app_secret_key):
    """
    This function will verify the integrity and authenticity of the callback received
    
    :param callback: callback received from facebook
    :param signature: X-hub-signature of the request
    :param app_secret_key: facebook app secret key. You can find it on your app page
    :return: True if signature matches else returns false
    
    """

    method, sign = signature.split("=")
    """
    Now a key will be created of callback using app secret as the key.
    And compared with xsignature found in the the headers of the request.
    If both the keys match then the function will run further otherwise it will halt
    """
    hmac_object = hmac.new(app_secret_key.encode("utf-8"), callback, "sha1")
    key = hmac_object.hexdigest()
    return hmac.compare_digest(sign, key)


class HttpApi:

    def __init__(self, verify_token, app_secret_key):
        self.text_handlers = []
        self.attachment_handlers = []
        self.postback_handlers = []
        self.verify_token = verify_token
        self.app_secret_key = app_secret_key

    def _on_get(self, req, resp):
        if req.get_param("hub.verify_token") == self.verify_token:
            resp.status = falcon.HTTP_200
            resp.body = req.get_param('hub.challenge')
        else:
            resp.status = falcon.HTTP_200
            resp.body = "Failed validation. Make sure the validation tokens match."

    def _on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = "success"
        signature = req.get_header("X-Hub-Signature")
        data = req.stream.read()
        verify_result = True  # verification of the callback is optional currently.
        # Therefore if no app secret key is passed then the bot will run anyway
        if self.app_secret_key is not None:
            verify_result = _verify(data, signature, self.app_secret_key)
        if verify_result:
            callback = json.loads(data)
            web = updates(callback)
            for message in web:  # Sometimes there are more than one number of callbacks.
                self.dispatch_handlers(message)

    def add_text_handler(self, func, text=None, position=None):
        _handler = text_handler(text, position)
        self.text_handlers.append(_handler())

    def add_attachment_handler(self, func, attachment_type=None):
        self.attachment_handlers.append((attachment_handler(func), attachment_type))

    def add_postback_handler(self, func):
        self.postback_handlers.append(func)

    def dispatch_handlers(self, message):
        for each_handler in self.text_handlers:
            each_handler(message)
        for each_attach_handler, attach_type in self.attachment_handlers:
            each_attach_handler(message, attach_type)
        for each_post_handler in self.postback_handlers:
            each_post_handler(message)

    def get_webhook_app(self):
        app = falcon.API()
        self.on_get = self._on_get
        self.on_post = self._on_post
        app.add_route("/", self)
        return app
