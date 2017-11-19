import logging
import re
from functools import wraps


def text_handler(text=None, position=None):
    def text_handle(func):

        @wraps(func)
        def handler(message):
            logger = logging.getLogger("handlers.text_handler.text_handle.handler")
            logger.setLevel(logging.ERROR)
            positions = {"start", "end", "contains", "is"}
            if message.message_received.text:
                msg = message.message_received.text
                logger.error(msg)
                if text:
                    logger.error(text)
                    esc_text = re.escape(text)
                    if position in positions:
                        match = None
                        if position == "starts":
                            regex = r'^' + esc_text
                            match = re.search(regex, msg)
                        elif position == "ends":
                            regex = esc_text + r'$'
                            match = re.search(regex, msg)
                        elif position == "contains":
                            match = re.search(esc_text, msg)
                        elif position == "is" and text == msg:
                            match = True
                        if match:
                            return func(message, text, position)
                else:
                    return func(message)

        return handler

    return text_handle


def attachment_handler(func):
    @wraps(func)
    def handler(message, attachment_type=None):
        if message.message_received.attachments:
            if attachment_type:
                if message.message_received.attachments.type == attachment_type:
                    return func(message, attachment_type)
            else:
                return func(message)

    return handler


def postback_handler(func):
    @wraps(func)
    def handler(message):
        if message.message_received.postback:
            return func(message)

    return handler
