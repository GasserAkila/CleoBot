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

df = pd.read_csv('responses.csv')

# print (type(query))
# resp = json.loads(query)

# Inquiry = parsed_string[1]['Inquire']
# intent  = list(Inquiry[0].values())[1]
# Tariffs  = parsed_string[1]['Tariffs']
# exact_tariff = list(Tariffs[0].values())[1]






# df1 = df.loc[df["product"]==exact_tariff]
# response = df1.loc[df1["intent_value"]==intent]['response']


# print(response)



x = df[df['Intent'] == entity and df['Product'] == product]
