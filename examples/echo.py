import os

import Facebook
import cherrpy
from paste.translogger import TransLogger

Page_Access_Token = ""  #Page access token; Required for sending the response
verify_token = ""       #Needed initially for verifying the webhook
app_secret_key = ""     #required for verifying the incoming payload. It's optional

def main(message):
    """
    This function receives the message as an arguement and echo back the text,image,video or audio
    """
    id = message.user_id
    sent = Facebook.send(Page_Access_Token)
    if message.message_received.text is not None:
        mess = message.message_received.text
        sent.sender_action(id)  #Sender action for message read
        sent.sender_action(id, action="typing_on")  #Sender action of type typing on
        sent.send_text(id, mess)    #Sends the text to the user
    elif message.message_received.attachments is not None:
        type = message.message_received.attachments.type
        url = message.message_received.attachments.url
        sent.send_attachment(id, type, url)

#The method is below for starting with cherrpy server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', '5000'))
    app = webhook.http(main,verify_token,app_secret_key)
    Facebook.start_server(main, host="0.0.0.0", port=PORT)  #start the webhook with main function passes as an arguement
    app_logged = TransLogger(app)
    cherrypy.tree.graft(app_logged, '/')
    cherrypy.config.update({
        'engine.autoreload_on': True,
        'log.screen': True,
        'server.socket_port': port,
        'server.socket_host': '0.0.0.0'
    })
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
