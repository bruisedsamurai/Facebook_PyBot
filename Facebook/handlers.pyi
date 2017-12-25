import enum
from typing import Union, Callable, Optional, Any

from .message import Message


class Position(enum.Enum):
    ...


def text_handler(text: str = None, position=Union[str, 'Position']) -> Callable[..., Callable]:
    function_type = Callable[[Message, ], Any]

    def text_handle(func: function_type) -> Callable[[Message, ], Optional[function_type]]:
        def handle(message: Message) -> Optional[function_type]:
            ...

        return handle

    return text_handle


attch_type = Callable[[Message, Optional[str]], Any]


def attachment_handler(func: attch_type) -> Callable[[Message, Optional[str]], Optional[attch_type]]:
    def handler(message: Message, attachment_type: str = None) -> Optional[attch_type]:
        ...

    return handler


postback_type = Callable[[Message, ], Any]


def postback_handler(func: postback_type) -> Callable[[Message, ], Optional[Callable[[Message], Any]]]:
    def handler(message: Message) -> Optional[postback_type]:
        ...

    return handler
