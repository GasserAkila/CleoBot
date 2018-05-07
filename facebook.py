from flask import Flask
from flask import request
from flask import json
from wit import Wit
import requests
import logging
import json
import timeit
import threading

PAGE_ACCESS_TOKEN = 'EAAZAf7sCMUFYBAB5bqRBRhwwsRwqVCsnGMqYDB64Tjc5SXUjPJaSnIPWWdlzaFTAlKWCu3ZBSdnLRvxzXPfoBl5KL29t9BAAxtL6yFZCUvO8OQbZAsyLCAD0w4GsyZC69vmmZCAelXnGiEOGZByZCZCeZCXZA9hxICAS0E0AAiQ1HnLKwZDZD'
auth = {'access_token': PAGE_ACCESS_TOKEN}
M_URL = 'https://graph.facebook.com/v2.6/me/messages'
C_URL = 'https://graph.facebook.com/v2.6/'


def WitTest(post, owner):
    token = '7F63TXDBHOOOTQZ52MM5PALSEWPMXA6F'
    wit_client = Wit(token)
    wit_client.logger.setLevel(logging.DEBUG)
    print("Hello1")
    resp = wit_client.message(post)

    print("Hello2")
    return ('Yay, got Wit.ai response: ' + str(resp))



def handleMessage(data):
    fb_senderid = data['entry'][0]['messaging'][0]['sender']['id']
    #fb_messageid = data['entry'][0]['id']
    msg = "Hello. Thanks for your message."
    payload = {
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': fb_senderid
        },
        'message': {
            'text': msg
        }
    }
    r = requests.post(M_URL, params=auth, json=payload)
    return


def handleComment(data):
    fb_username = data['entry'][0]['changes'][0]['value']['from']['name']
    fb_postid = data['entry'][0]['changes'][0]['value']['post_id']
    fb_post = data['entry'][0]['changes'][0]['value']['message']
    # print ("I'm here")
    resp = WitTest(fb_post, fb_username)
    msg = "Hello " + fb_username + ". Thanks for your posts. ya 7amoksha"
    cURL = C_URL + fb_postid + "/comments"
    payload = {
        'message': msg
    }
    r = requests.post(cURL, params=auth, json=payload)
    # print ("I'm there")
    return


app = Flask(__name__)

@app.route("/", methods=['GET'])
def verify():
    challenge = request.args.get("hub.challenge")
    if challenge:
        return challenge
    else:
        return "Ok"


@app.route("/", methods=['POST'])
def webhook():
    #convert json response to dict
    in_data = request.get_json()

    # f = open("post.json","a")
    # f.write(json.dumps(in_data))
    # f.write("\n\n")
    # f.close()

    #Messanger
    try:
        if in_data['entry'][0]['messaging'][0]['message']['text']:
            handleMessage(in_data)
            return "Ok"
    except KeyError:
        pass

    #Post
    try:
        if in_data['entry'][0]['changes'][0]['field'] == "feed" and in_data['entry'][0]['changes'][0]['value']['item'] == "post":

            start = timeit.default_timer()

            wit_thread = threading.Thread(target=handleComment, args=[in_data])
            # wit_thread.join()
            wit_thread.start()

            stop = timeit.default_timer()

            print (stop - start)


            return "Ok"
    except KeyError:
        pass

    return "Ok"


if __name__ == "__main__":
    app.run()
