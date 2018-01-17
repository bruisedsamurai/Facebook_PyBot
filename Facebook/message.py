try:
    import ujson as json
except ImportError:
    import json  # type: ignore


def updates(callback):
    """
    This function takes the callback as an input and creates an instance for each message received and stores
    it(instance) into an array. Which is then returned
    
    :param callback: contains the callback from facebook.
    :return: array of Message instances.
    
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

        :param data: Message containing callback from facebook i.e. sender_id,recipient_id,message etc.
        :type data: Dict

        Attributes:
            user_id(:obj:'int') user id of the facebook user.
            page_id(:obj:'int') page id of the recipient bot.
            message_received(:class:`Received`): instance of Received class.
            message_delivered(:class:`Delivered`):
            message_read(:class:`Read`):
        
        """
        self.user_id = str(data['sender']['id'])
        self.page_id = data['recipient']['id']
        # Thing may fuck up a little below, cause I dunno if "is_echo" is always there or just in echo callbacks
        # TODO: Check echo callbacks

        self.message_received = Received(data)
        try:
            self.message_echo = Echo(data)
            # if self.Message_Echo.echo is not None:
            # self.Message_Received.message = None
        except KeyError:
            pass
        self.message_delivered = Delivered(data)
        self.message_read = Read(data)

    def __repr__(self):
        if self.message_received:
            obj = repr(self.message_received)
        elif self.message_delivered:
            obj = repr(self.message_delivered)
        elif self.message_read:
            obj = repr(self.message_read)
        else:
            obj = ""
        return "Message({},{},{})".format(
            self.user_id, self.page_id, obj)


class Received:
    """
    Message Received callback
    
    This class stores the text or attachment sent by facebook in the callback.
    
    Attributes:
        mid(:obj:'str') Message id of the message received. Be it either text or attachment.
        text(:obj:'str'): Optional.stores the text of the message if received(otherwise none).
        attachments(:obj:'list'): Optional.list of instance of the attachment class.
        quick_reply_payload: Optional.The data received in the callback. It is received when quick replies are
          tapped and it's content depends on the postback data sent in developer payload.
        postback_payload: Optional.The postback data received in the callback

    
    For more info go to https://developers.facebook.com/docs/messenger-platform/webhook-reference/message
    """

    def __init__(self, messaging):
        self.mid = self.text = self.quick_reply = None
        self.attachments = None
        self.message = None
        self.postback = None
        self.referral = None
        if messaging.get('message'):
            self.message = messaging['message']
            self.mid = self.message['mid']
            if self.message.get('text'):  # If a text message is received then the message will be stored
                self.text = self.message['text']
            elif self.message.get('attachments'):  # an array of attachments is stored here
                self.attachments = []
                for eachAttachment in self.message['attachments']:
                    self.attachments.append(Attachments(eachAttachment))
            if self.message.get('quick_reply'):
                self.quick_reply = self.message['quick_reply']
                self.quick_reply_payload = self.quick_reply['payload']
        elif messaging.get("postback"):
            self.postback = messaging["postback"]
            self.postback_payload = self.postback.get("payload")
            self.referral = self.postback.get("referral")

    def __repr__(self):
        msg_type = "text" if self.text else self.attachments.type
        return "Received(%r,%r)" % (self.mid, msg_type)

    def __bool__(self):
        if self.message or self.postback:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.text:
            return self.text == other.text
        elif self.attachments:
            return self.attachments == other.attachments
        elif self.postback == other.postback:
            return self.postback_payload == other.postback_payload


class Delivered:
    """
    Message Delivered callback
        
    For more info go to https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-delivered

    Attributes:
        mids: List containing message IDs of messages that were delivered. Field may not be present.
        watermark: All messages that were sent before this timestamp were delivered.
        seq: Sequence number.

    If a delivery callback is received then it will be stored otherwise delivery will be none
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
            self.seq = None

    def __bool__(self):
        if self.delivery:
            return True
        else:
            return False


class Read:
    """
    Message Read Callback

    For more info go to https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-read

    If a read callback is received then it will be stored otherwise read will be none
    """

    def __init__(self, messaging):
        if 'read' in messaging:
            self.read = messaging['read']
            self.Watermark = self.read['watermark']
            self.Seq = self.read['seq']
        else:
            self.Watermark = None
            self.read = None
            self.Seq = None

    def __bool__(self):
        if self.read:
            return True
        else:
            return False


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


class Attachments:
    """
    This class contains the type of the attachments and their payload

    Attributes:
        type(str): The type of attachment. Will be one of many type : location, image,video,audio or file.
        url(str): Optional.URL of the image,video,audio or file.
        coordinates_lat(int): Optional.latitude of the coordinate of the location received.
        coordinates_long(int): Optional.longitude of the coordinate of the location.

    """

    def __init__(self, attachment):
        self.type = attachment['type']
        self.url = None
        if self.type == 'location':
            self.title = attachment["title"]
            self.coordinates_lat = attachment['payload']['coordinates']['lat']
            self.coordinates_long = attachment['payload']['coordinates']['long']
        else:
            self.url = attachment['payload']['url']

    def __bool__(self):
        if self.type:
            return True
        else:
            return False

    def __repr__(self):
        if self.type == "location":
            sec_arg = self.coordinates_lat + "," + self.coordinates_long
        else:
            sec_arg = self.url
        return "Attachments({},{})".format(self.type, sec_arg)

    def __eq__(self, other):
        if self.type == "location":
            sec_arg_self = self.coordinates_lat + "," + self.coordinates_long
            sec_arg_other = other.coordinates_lat + "," + other.coordinates_long
            equality = sec_arg_self == sec_arg_other
        else:
            equality = self.url == other.url
        return equality and self.type
