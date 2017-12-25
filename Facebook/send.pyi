from typing import Dict, List, Optional, Any, Union


class Send:
    def __init__(self, page_access_token: str, api_ver: int = None) -> None:
        ...

    def send_text(self, user_id: Union[str, int], message: str, notification_type: str = 'REGULAR',
                  quick_replies: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        url: str = ...
        params: Dict[str, Any] = ...
        header: Dict[str, Any] = ...

        payload: Dict[str, Any] = ...

        result: Dict[str, Any] = ...

        return ...

    def send_attachment(self, user_id: Union[str, int], attachment_type: str, url: str, file,
                        notification_type: str = 'REGULAR',
                        quick_replies: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        ...

    def sender_action(self, user_id: Union[str, int], action: str = "mark_seen") -> Optional[Dict[str, Any]]:
        ...

    def get_user_info(self, user_id: Union[str, int]) -> Optional[Dict[str, Any]]:
        ...

    def send_button_template(self, user_id: Union[str, int], text: str, button_1: Dict[str, Any],
                             button_2: Dict[str, Any] = None,
                             button_3: Dict[str, Any] = None, quick_replies: Dict[str, Any] = None) -> Optional[
        Dict[str, Any]]:
        ...

    def send_generic_template(self, user_id: Union[str, int], elements: List[Dict[str, Any]],
                              quick_replies: Dict[str, Any] = None) -> \
            Optional[Dict[str, Any]]:
        ...

    def send_list_template(self, user_id: Union[str, int], elements: List[Dict[str, Any]],
                           top_element_style: str = "large",
                           quick_replies: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        ...
