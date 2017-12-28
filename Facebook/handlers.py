import enum
import logging
import re
from functools import wraps


class Position(enum.Enum):
    """
    Enumerates for the position of the text in text_handler
    """
    START = "start"
    END = "end"
    CONTAINS = "contains"
    IS = "is"


def text_handler(text=None, position=None):
    """
    Text handler which runs the decorated function if the message from facebook consists of the text with required
    position(if passed)

    @optional

    :param text: text to be searched in the facebook text message.
    :type text: str
    :param position: position of the text in the message.
    :type position: enumerate,str
    :return: text_handle.
    :rtype: callable
    """

    def text_handle(func):
        """
        takes the decorated function as argument and returns a function
        :param func: function to be run if cases matched
        :return: handler
        """

        @wraps(func)
        def handler(message):
            logger = logging.getLogger("handlers.text_handler.text_handle.handler")
            logger.setLevel(logging.INFO)
            positions = {Position.START, Position.CONTAINS, Position.END, Position.IS, "start", "is", "contains", "end"}
            if message.message_received.text:
                msg = message.message_received.text
                if text:
                    match = False
                    logger.error(text)
                    esc_text = re.escape(text)
                    if position:
                        if position in positions:
                            if position == (Position.START or "start"):
                                regex = r'^' + esc_text
                                match = re.search(regex, msg)
                            elif position == (Position.END or "end"):
                                regex = esc_text + r'$'
                                match = re.search(regex, msg)
                            elif position == (Position.CONTAINS or "contains"):
                                match = re.search(esc_text, msg)
                            elif position == (Position.IS or "is") and text == msg:
                                match = True
                    else:
                        match = re.search(esc_text, msg)
                    if match:
                        return func(message)
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
