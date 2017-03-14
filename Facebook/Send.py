import os
import ujson

import requests

from exception import raiseError

headers = {"Content-Type": "application/json"}


class send:
    def __init__(self, Page_Access_Token):
        self.URL = 'https://graph.facebook.com/v2.8/{}'
        self.Access_Token = Page_Access_Token

    def send_text(self, User_id, message, notification_type='REGULAR'):
        """
        @optional
        sender_action
        @required
        :param User_id: user_id of the recipient
        :type User_id: string
        :param message: Message text
        :type message: string
        :param notification_type: Push notification type: REGULAR, SILENT_PUSH, or NO_PUSH
        :type notification_type: string
        :return: return response from facebook or type of error if encountered
        """
        URL = self.URL.format("me/messages")
        payload = {}
        params = {"access_token": self.Access_Token}
        headers = {"Content-Type": "application/json"}
        payload['recipient'] = {"id": User_id}
        payload['message'] = {"text": message}
        payload["notification_type"] = notification_type
        response = requests.post(URL, headers=headers, params=params, data=ujson.dumps(payload))
        result = response.json()
        print(result)
        if 'recipient_id' not in result:
            error = raiseError(result)
            raise error
        else:
            return result

    def send_attachment(self, User_id, type, url=None, file=None, notification_type='REGULAR'):
        """
        @required
        :param User_id: user_id of the recipient
        :param type: Type of attachment, may be image, audio, video, file or template
        :type type: str
        :param url: URL of data
        :param notification_type: Push notification type: REGULAR, SILENT_PUSH, or NO_PUSH
        :type notification_type: string
        :return: response from facebook or type of error if encountered
        """

        payload = {
            "recipient": {
                "id": User_id
            },
            "message": {
                "attachment": {
                    "type": type,
                    "payload": {}
                }
            },
        }
        if url is not None:
            payload["message"]["attachment"]["payload"]["url"] = url
        else:
            payload["filedata"] = (os.path.basename(file), open(file, 'rb'))
        payload["notification_type"] = notification_type
        params = {"access_token": self.Access_Token}
        URL = self.URL.format("me/messages")
        response = requests.post(URL, headers=headers, params=params, data=ujson.dumps(payload))
        result = response.json()
        if "recipient_id" not in result:
            error = raiseError(result)
            raise error
        else:
            return result

    def sender_action(self, User_id, action="mark_seen"):
        """
        Sender Action of Facebook bot API.
        For more info https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions
        :param User_id:   User id of the person who is going to receive the action
        :type User_id:
        :param action: type of sender action
        :type action: str
        """
        if not isinstance(action, str):
            raise ValueError
        payload = {
            "recipient": {
                "id": User_id
            },
            "sender_action": action
        }
        URL = self.URL.format("me/messages")
        param = {"access_token": self.Access_Token}
        response = requests.post(URL, headers=headers, params=param, data=ujson.dumps(payload))
        data = response.json()
        return data

    def get_UserInfo(self, User_id):
        """
        for more info go to https://developers.facebook.com/docs/messenger-platform/user-profile
        :param User_id: User id of the person of whom user info is to be retrieved
        :type User_id:
        :return: first name,last name,profile pic,locale,timezone,gender
        """
        URL = self.URL.format(User_id)
        key = {"fields": "first_name,last_name,profile_pic,locale,timezone,gender",
               "access_token": self.Access_Token
               }
        response = requests.get(URL, params=key)
        data = response.json()
        try:
            data = ujson.decode(data)
        except:
            pass
        if data.get["first_name"]:
            return data["first_name"], data["last_name"], data["profile_pic"], data["locale"], data["timezone"], data[
                "gender"]
        else:
            return None

    def sendButton_template(self, User_id, text, Button_1, Button_2=None, Button_3=None):
        """
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template
        :param User_id: User Id of the recipient to whom the message is being sent
        :param text: UTF-8 encoded text of up to 640 characters that appears the in main body
        :param Button_1,Button_2,Button_3:  Set of, one to three, buttons that appear as call-to-actions.
        :return:
        """
        try:
            Button_1 = ujson.loads(Button_1)
            Button_2 = ujson.loads(Button_2)
            Button_3 = ujson.loads(Button_3)
        except:
            pass
        buttons = [Button_1]
        if Button_2 is not None:
            buttons.append(Button_2)
        if Button_3 is not None:
            buttons.append(Button_3)
        payload = {
            "recipient": {
                "id": User_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons
                    }
                }
            }
        }
        URL = self.URL.format("me/messages")
        params = {"access_token": self.Access_Token}
        response = requests.post(URL, headers=headers, params=params, data=ujson.dumps(payload))
        data = response.json()
        if not data.get("recipient_id"):
            error = raiseError(data)
            raise error
        else:
            return data

    def sendGeneric_Template(self, User_id, *args):
        """
        For more info go to https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template
        :param User_id: User Id of the recipient to whom the message is being sent
        :type User_id:
        :param args: a set of elements(up to 10).
        Element:Data for each bubble in message
        :return:
        """
        elements = []
        for arg in args:
            elements.append(arg)
        payload = {
            "recipient": {
                "id": User_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "image_aspect_ratio": "horizontal",
                        "elements": elements
                    }
                }
            }
        }
        print(payload)
        URL = self.URL.format("me/messages")
        params = {"access_token": self.Access_Token}
        response = requests.post(URL, headers=headers, params=params, data=ujson.dumps(payload))
        data = response.json()
        if not data.get("recipient_id"):
            error = raiseError(data)
            raise error
        else:
            return data

    def sendList_template(self, User_id, top_element_style="large", *args):
        """
        For more info go to https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template
        :param User_id: User Id of the recipient to whom the message is being sent
        :type User_id: str
        :param top_element_style:Value must be large or compact. Default to large if not specified
        :type top_element_style: enum
        :param args:List view elements (maximum of 4 elements and minimum of 2 elements)
        :return:
        """
        elements = []
        for arg in args:
            elements.append(arg)
        payload = {
            "recipient": {
                "id": User_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "list",
                        "top_element_style": top_element_style,
                        "elements": elements
                    }
                }
            }
        }
        print(payload)
        URL = self.URL.format("me/messages")
        params = {"access_token": self.Access_Token}
        response = requests.post(URL, headers=headers, params=params, data=ujson.dumps(payload))
        data = response.json()
        if not data.get("recipient_id"):
            error = raiseError(data)
            raise error
        else:
            return data
