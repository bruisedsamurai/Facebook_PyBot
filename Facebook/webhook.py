import hmac
import logging
import traceback
from threading import Thread

import falcon

try:
    import ujson as json
except:
    import json

from .message import updates

logger = logging.getLogger(__name__)


def http(main_func=None, verify_token=None, app_secret_key=None):
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
                for message in web:  # Sometimes there are more than one number of callbacks.
                    _run(main_func, message)

    api = HttpApi()
    app.add_route('/', api)
    return app


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
