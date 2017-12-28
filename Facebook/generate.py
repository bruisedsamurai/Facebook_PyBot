from .exception import CharacterCountExceeded


class Generate:
    @staticmethod
    def button(button_type, title="None", url=None, payload=None, webview_height="full"):
        """
        Creates a button and returns the dictionary containing the button data

        .. seealso:https://developers.facebook.com/docs/messenger-platform/send-api-reference/buttons
        For more info https://developers.facebook.com/docs/messenger-platform/send-api-reference/buttons

        :arg button_type: Type of button.
        :type button_type: str
        :arg title: Title of the button. Max 20 characters.
        :type title: str
        :arg url: This URL is opened in a mobile browser when the button is tapped.
        :type url: str
        :arg payload: This data will be sent back to your webhook. 1000 character limit.
        :type payload: str
        :arg webview_height: Height of the Webview. Valid values: compact,tall,full.
        :type webview_height: str

        :returns: A dictionary containing mapping between proper keys and arguments.
        :rtype: dict


        """
        if len(payload) > 1000:
            raise CharacterCountExceeded("Max number of characters allowed are 1000."
                                         "The number of characters in the 'payload' are %s. " % len(payload))
        button = {
            "type": type,
            "title": title,
        }
        if button_type == "web_url":
            button["url"] = url
            button["webview_height_ratio"] = webview_height
        elif button_type == "postback":
            button["payload"] = payload
        elif button_type == "phone_number":
            button["payload"] = payload
        elif button_type == "element_share":
            button.pop("title")
        elif button_type == "account_link":
            button["url"] = url
            button.pop("title")
        elif button_type == "account_unlink":
            button.pop("title")
        return button

    @staticmethod
    def element(title, subtitle=None, image_url=None, buttons=None):
        """
        Generates payload for element
        
        :param title: Bubble title.
        :type title: str
        :param subtitle: Bubble subtitle.
        :type subtitle: str
        :param image_url: Bubble image.
        :type image_url: str
        :param buttons: Set of buttons that appear as call-to-actions.
        :type buttons: list

        :return: A dictionary containing mapping between proper keys and arguments.
        :rtype: dict
        
        """
        element = {
            "title": title,
            "subtitle": subtitle,
            "image_url": image_url,
        }
        if subtitle is None:
            element.pop("subtitle")
        if image_url is None:
            element.pop("image_url")
        if buttons is not None:
            element["buttons"] = buttons
            print(buttons)
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
        :rtype: dict
        
        """
        quick_reply = {
            "content_type": content_type,
        }
        if content_type == "text":
            if (title or payload) is None:
                raise ValueError
            quick_reply["title"] = title
            quick_reply["payload"] = payload
            quick_reply["image_url"] = image_url
        return quick_reply
