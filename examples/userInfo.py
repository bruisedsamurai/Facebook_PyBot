"""
Gets the user info and sendback to the user in the form of template form on being asked
This program not teaches the use of getting user info but also how to send a generic template message
"""
import os

import Facebook

def main(message):
	id=message.user_id
	sent=Facebook.send(PAGE_ACCESS_TOKEN)
	if message.message_received.text is not None:
		mess=message.message_received.text
		if mess == "get me":
			"""
			get_UserInfo returns the first name,last name,url of the picture,their locale,timezone and gender of person whom id is passed as an arguement
			"""
        	fname, lname, picurl, locale, tz, gender = sent.get_UserInfo(id)
        	ele = generate.element(fname + " " + lname, gender + '\n' + locale, picurl)
        	sent.send_generic_template(id, ele)


if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', '5000'))
    app = webhook.http(main,verify_token,app_secret_key)  #start the webhook with main function passes as an arguement
        
