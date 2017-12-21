from typing import Dict, Any, List


class Generate:
    @staticmethod
    def button(button_type: str, title: str = None, payload: str = None, webview_height: str = "full") -> Dict[
        str, str]:
        ...

    @staticmethod
    def element(title: str, subtitle: str = None, image_url: str = None, buttons: List[Dict[str, Any]] = None) -> Dict[
        str, Any]:
        ...

    @staticmethod
    def quick_reply(content_type: str, title: str = None, payload: str = None, image_url: str = None) -> Dict[str, str]:
        ...
