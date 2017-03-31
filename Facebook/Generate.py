class generate:
    def button(self, type, title="None", url=None, payload=None, webview_height="full"):
        """
        For more info https://developers.facebook.com/docs/messenger-platform/send-api-reference/buttons
        
        :param type: Type of button.
        :type type: str
        :param title: Button title. 20 character limit.
        :type title: str
        :param url:This URL is opened in a mobile browser when the button is tapped
        :type url: str
        :param payload:This data will be sent back to your webhook. 1000 character limit.
        :type payload:str
        :param webview_height:Height of the Webview. Valid values: compact, tall, full.
        :type webview_height:enumerate
        :return: dict of button
        
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

    def element(self, title, subtitle, image_url, *args):
        """
        Generates payload for element
        
        :param title:Bubble title
        :type title: str
        :param subtitle:Bubble subtitle
        :type subtitle: str
        :param image_url:Bubble image
        :type image_url: str
        :param args:Set of buttons that appear as call-to-actions
        :type args:Array of button
        :return: dict of element
        
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
        return element
