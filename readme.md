Readme:

#Project Title

Facebook_PyBot

## Description
This is an Unofficial Facebook bot API in python. Facebook Bots can be build using this library.


## Installing
Using pip:

'''
pip install python_facebook_bot_api
'''

Or install from the source with:

'''
$ git clone https://github.com/hundredeir/Facebook_PyBot
$ cd Facebook_Pybot
$ python setup.py install
'''
## Getting Started

First of all you have to create an App and a page on facebook platform.
But, before you create them. We should first setup the webhook.

create a new script and write:

'''
import os
from facebook import webhook
'''

then create a new Verify Token; It can be alphanumeric. And store it in a variable named.
'''
Token="user generated token"
'''
Now, add anothers lines to the script
'''
PORT = int(os.environ.get('PORT', '5000'))
webhook.startServer(Verify_Token=Token,port=PORT)
'''

Tip:
>For the non initiated you can use a heroku service for hosting your bots. Which provides to host the app and also comes with a free plan.
>Guide for setting up hosting is given here https://devcenter.heroku.com/articles/getting-started-with-python#introduction
>Note: Since, we are using cherrpy instead of gunicorn. You only to type the line below in your procfile
'''
web: python yourscript.py
'''

Now, you can go ahead and create a Facebook page and App
Facebook provides a guide for that:	https://developers.facebook.com/docs/messenger-platform/guides/setup


After the verification is done, You can create your script torun bots. A few examples are given in the repository

Note: This wrapper is still in alpha. Even though everything is working but things may change for the improvement of the module.

A wiki is in work in progress