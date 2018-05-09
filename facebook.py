from flask import Flask
from flask import request
from flask import json
from wit import Wit
import requests
import logging
import json
import timeit
import threading
import pandas as pd
from random import *
from googletrans import Translator

PAGE_ACCESS_TOKEN = 'EAAZAf7sCMUFYBAB5bqRBRhwwsRwqVCsnGMqYDB64Tjc5SXUjPJaSnIPWWdlzaFTAlKWCu3ZBSdnLRvxzXPfoBl5KL29t9BAAxtL6yFZCUvO8OQbZAsyLCAD0w4GsyZC69vmmZCAelXnGiEOGZByZCZCeZCXZA9hxICAS0E0AAiQ1HnLKwZDZD'
auth = {'access_token': PAGE_ACCESS_TOKEN}
M_URL = 'https://graph.facebook.com/v2.6/me/messages'
C_URL = 'https://graph.facebook.com/v2.6/'


def generateResonse(response,owner, language):

    df = pd.read_csv('responses.csv')
    comment = "Thanks for you message, We will get back to you shortly :)"
    entities = response['entities']
    intent = ""
    product = ""
    # print (entities['Tariffs'])
    try:

        for entity in entities:
            print (entity)
            if any(df.Intent == entity):
                if (intent == ""):
                    intent = entity
                    print ("Intent", intent)
                # continue
                # products = df.loc[df['Intent'] == entity]]
            if ((entity == "Tariffs" or entity == "product" or entity == "network") and any(df.Product == entities[entity][0]['value'])):
                    product = entities[entity][0]['value']
                    print ("Product", product)

        if (intent != ""):
            if ((intent == "greetings") | (intent == "goodbye")):
                comments = list(df[df['Intent'] == intent]['Response'])[0]
                comments_splitted = comments.split('|')
                print (comments)
                if (language == 'en'):
                    comment = comments_splitted[0]
                if (language == 'ar'):
                    comment = comments_splitted[1]
            else:
                # products =
                comments = list(df.loc[(df['Intent'] == intent) & (df['Product'] == product)]['Response'])[0]
                comments_splitted = comments.split('|')
                print (comments)
                if (language == 'en'):
                    comment = comments_splitted[0]
                if (language == 'ar'):
                    comment = comments_splitted[1]

        # print(df.head())

    # print("be5")
    except:
        if (language == 'en'):
            print("Thanks for you message, We will get back to you shortly :)")
        if (language == 'ar'):
            print("عفواً سيتم التواصل معك من خلال مندوب فودافون")


    print(comment)
    return comment;

def WitTest(post, owner):
    token = '7F63TXDBHOOOTQZ52MM5PALSEWPMXA6F'
    wit_client = Wit(token)
    wit_client.logger.setLevel(logging.DEBUG)
    print("Hello1")

    resp = wit_client.message(post)
    translator = Translator()
    lang = translator.detect(post).lang
    print("Hello2 this post is ", lang)
    comment = generateResonse(resp, owner, lang)
    print("Hello3")
    print(comment)

    return comment



def handleMessage(data):
    fb_senderid = data['entry'][0]['messaging'][0]['sender']['id']
    # fb_messageid = data['entry'][0]['id']
    fb_msg = data['entry'][0]['messaging'][0]['message']['text']
    comment = WitTest(fb_msg, fb_senderid)
    msg = comment
    #msg = "Hello. Thanks for your message."
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
    comment = WitTest(fb_post, fb_username)
    translator2 = Translator()
    lang = translator2.detect(comment).lang
    if (lang ==  'en'):
        msg = "Hello " + fb_username + ". " + comment
    if (lang ==  'ar'):
        msg = "أهلاً " + fb_username + ". " + comment
    # msg = comment
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
            # print ("message")
            wit_thread = threading.Thread(target=handleMessage, args=[in_data])
            wit_thread.start()
            # handleMessage(in_data)
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
