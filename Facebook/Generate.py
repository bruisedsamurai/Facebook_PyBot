class Generate:
    @staticmethod
    def button(type, title="None", url=None, payload=None, webview_height="full"):
        """
        For more info https://developers.facebook.com/docs/messenger-platform/send-api-reference/buttons
        
        :param type: Type of button.
        :type type: str
        :param title: Button title. 20 character limit.
        :type title: str
        :param url: This URL is opened in a mobile browser when the button is tapped.
        :type url: str
        :param payload: This data will be sent back to your webhook. 1000 character limit.
        :type payload: str
        :param webview_height: Height of the Webview. Valid values: compact, tall, full.
        :type webview_height: enumerate
        :return: dict of button.
        
        """
        button = {
            "type": type,
            "title": title,
        }
        if type == "web_url":
            button["url"] = url
            button["webview_height_ratio"] = webview_height
        elif type == "postback":
            button["payload"] = payload
        elif type == "phone_number":
            button["payload"] = payload
        elif type == "element_share":
            button.pop("title")
        elif type == "account_link":
            button["url"] = url
            button.pop("title")
        elif type == "account_unlink":
            button.pop("title")
        return button

    @staticmethod
    def element(title, subtitle, image_url, *args):
        """
        Generates payload for element
        
        :param title: Bubble title.
        :type title: str
        :param subtitle: Bubble subtitle.
        :type subtitle: str
        :param image_url: Bubble image.
        :type image_url: str
        :param args: Set of buttons that appear as call-to-actions.
        :type args: Array of button
        :return: dict of element.
        
        """
        element = {
            "title": title,
            "subtitle": subtitle,
            "image_url": image_url,
        }
        if args:
            buttons = []
            for button in args:
                buttons.append(button)
            element["buttons"] = buttons
        print(element)
        return element

    @staticmethod
    def quick_reply(content_type, title=None, payload=None, image_url=None):
        """
        This method creates a dict for a quick_reply
        
        :param content_type: text or location
        :type content_type: str
        :param title: Caption of button
        :type title: str
        :param payload: Custom data that will be sent back to you via webhook
        :type payload: str
        :param image_url: URL of image for text quick replies
        :type image_url: str
        :return: dict containing quick_reply
        
        """
        quick_reply = {
            "content_type": content_type,
        }
        if content_type == "text":
            if title or payload is None:
                raise ValueError
            quick_reply["title"] = title
            quick_reply["payload"] = payload
            quick_reply["image_url"] = image_url
        return quick_reply
