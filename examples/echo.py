import os

import Facebook

Page_Access_Token = ""  #Page access token; Required for sending the response

def main(message):
    """
    This function receives the message as an arguement and echo back the text,image,video or audio
    """
    id = message.USER_ID
    sent = Facebook.send(Page_Access_Token)
    if message.Message_Received.text is not None:
        mess = message.Message_Received.text
        sent.sender_action(id)  #Sender action for message read
        sent.sender_action(id, action="typing_on")  #Sender action of type typing on
        sent.send_text(id, mess)    #Sends the text to the user
    elif message.Message_Received.attachments is not None:
        type = message.Message_Received.attachments.type
        url = message.Message_Received.attachments.url
        sent.send_attachment(id, type, url)


if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', '5000'))
    Facebook.start_server(main, host="0.0.0.0", port=PORT)  #start the webhook with main function passes as an arguement
