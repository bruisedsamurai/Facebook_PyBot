try:
    import ujson as json
except:
    import json


def Updates(callback):
    """
    This function takes the callback as an input and creates an instance for each message received and stores it into
    an array. Which is then returned
    :param callback: contains the callback from facebook
    :return: array of Message instances
    """
    entries = []
    try:
        callback = json.decode(callback)
    except:
        pass
    for entry in callback["entry"]:
        messaging = entry["messaging"]
        messages = [Message(data) for data in messaging]
        entries.extend(messages)
    return entries


class Message:
    def __init__(self, data):
        """
        a class for webhooks which consists of
         1. USER_ID
         2. PAGE_ID
         Then three objects i.e Message_Received, Message_Delivered,Message_Read
         Message_Received callback occurs when a message is received by the webhook
         Message_Delivered callback when a message is delivered to the user
         Message_Read callback when the message is read by user
        :param data: Message containing sender_id,recipient_id,message etc
        :type data: Dict
        """
        self.USER_ID = str(data['sender']['id'])
        self.PAGE_ID = data['recipient']['id']
        # Thing may fuck up a little below, cause I dunno if "is_echo" is always there or just in echo callbacks
        # TODO: Check echo callbacks

        self.Message_Received = Received(data)
        try:
            self.Message_Echo = Echo(data)
            # if self.Message_Echo.echo is not None:
            # self.Message_Received.message = None
        except:
            pass
        self.Message_Delivered = Delivered(data)
        self.Message_Read = Read(data)


# TODO: add attachments in Received and echo classes

class Received:
    """
    Message Received callback
    For more info go to https://developers.facebook.com/docs/messenger-platform/webhook-reference/message
    """

    def __init__(self, messaging):
        self.mid = self.text = self.quick_reply = self.payload = None
        self.attachments = None
        if messaging.get('message'):
            message = messaging['message']
            self.mid = message['mid']
            if message.get('text'):
                self.text = message['text']
            elif message.get('quick_reply'):
                self.quick_reply = message['quick_reply']
                self.payload = self.quick_reply['payload']
            elif message.get('attachments'):  # an array of attachments is stored here
                # TODO: Attachments object looks like consisting of an array, Take a look at it later
                for eachAttachment in message['attachments']:
                    """
                    creates an instance of attachments class and stores it.
                    the instance will consist of either contain coordinates or either URL of the attachment
                    """
                    self.attachments = attachments(eachAttachment)


class Delivered:
    """
    Message Delivered callback
    For more info go to https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-delivered
    """

    def __init__(self, messaging):
        self.mids = []
        if 'delivery' in messaging:
            self.delivery = messaging['delivery']
            if self.delivery.get('mids'):
                for ids in self.delivery['mids']:
                    self.mids = self.mids.append(ids)
            self.watermark = self.delivery['watermark']
            self.seq = self.delivery['seq']
        else:
            self.delivery = None


class Read:
    """
    Message Read Callback
    For more info go to https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-read
    """

    def __init__(self, messaging):
        if 'read' in messaging:
            self.read = messaging['read']
            self.Watermark = self.read['watermark']
            self.Seq = self.read['seq']
        else:
            self.read = None


class Echo:
    """
    Message Echo callback
    For more info go to https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-echo
    """

    def __init__(self, messaging):
        self.message = messaging['message']
        if self.message.get('is_echo'):
            self.message = messaging['message']
            self.app_id = self.message['app_id']
            if self.message.get('metadata'):
                self.metadata = self.message['metadata']
            else:
                self.metadata = None
            self.mid = self.message['mid']
            self.seq = self.message['seq']
        else:
            self.echo = None


class attachments:
    """
    This class contains the type of the attachments and their payload
    """

    def __init__(self, attachment):
        self.type = attachment['type']
        # TODO: Make payload whole one variable
        if self.type == 'location':
            self.coordinates_lat = attachment['payload']['coordinates.lat']
            self.coordinates_long = attachment['payload']['coordinates.long']
        else:
            self.url = attachment['payload']['url']
