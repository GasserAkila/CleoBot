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
import json
# Post
# Greeting/Flex/MI


query = """{
  "_text": "i am having issues with my flex bundle",
  "entities": {
    "contact": [
      {
        "suggested": true,
        "confidence": 0.91528,
        "value": "my",
        "type": "value"
      }
    ],
    "Tariffs": [
      {
        "confidence": 0.95672915253402,
        "value": "Flex",
        "type": "value"
      }
    ],
    "product_features": [
      {
        "confidence": 0.96646603314698,
        "value": "bundle",
        "type": "value"
      }
    ],
    "complaint": [
      {
        "confidence": 0.9717014751606,
        "value": "complaint"
      }
    ]
  },
  "msg_id": "0SXbdPR53ZLUteqlh"
}"""




token = '7F63TXDBHOOOTQZ52MM5PALSEWPMXA6F'
wit_client = Wit(token)
wit_client.logger.setLevel(logging.DEBUG)
print("Hello1")

resp = wit_client.message(post)

print("Hello2")
comment = generateResonse(resp, owner)
print("Hello3")

return comment

df = pd.read_csv('responses.csv',dtype=str)
print (type(query))
resp = json.loads(query)

# Inquiry = parsed_string[1]['Inquire']
# intent  = list(Inquiry[0].values())[1]
# Tariffs  = parsed_string[1]['Tariffs']
# exact_tariff = list(Tariffs[0].values())[1]






# df1 = df.loc[df["product"]==exact_tariff]
# response = df1.loc[df1["intent_value"]==intent]['response']


# print(response)
