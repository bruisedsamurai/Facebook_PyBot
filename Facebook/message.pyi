from typing import Dict, Any, List

def updates(callback:Dict[str,Any])-> List[Dict[str,Any]]:
    ...

class Message:
    def __init__(self, data: Dict[str, Any]) -> None:
        ...
        self.message_received: Received = ...
        self.message_delivered: Delivered = ...
        self.message_read: Read = ...


class Received:
    def __init__(self, messaging: Dict[str, Any]) -> None:
        ...


class Delivered:
    def __init__(self, messaging: Dict[str, Any]) -> None:
        ...


class Read:
    def __init__(self, messaging: Dict[str, Any]) -> None:
        ...


class Attachments:
    def __init__(self, attachment: Dict[str, Any]) -> None:
        ...
