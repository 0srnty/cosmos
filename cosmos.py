#!/usr/bin/env python3
import azure.cosmos.cosmos_client as cosmos_client
import json
import base64
from array import array
import binascii
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template
import time
from datetime import datetime
import site
import cgi
import html


form = cgi.FieldStorage()
time = form.getfirst("TEXT_1", "не задано")
config = {
    'ENDPOINT': ,
    'PRIMARYKEY': ,
    'DATABASE': 'ibecomgw',
    'CONTAINER': 'ibecomgw'
}

client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={'masterKey': config['PRIMARYKEY']})
database_link = 'dbs/' + config['DATABASE']
db=client.ReadDatabase(database_link)
id= config['CONTAINER']
collection_link = database_link + '/colls/{0}'.format(id)
collection = client.ReadContainer(collection_link)
query =  { "query": "SELECT * FROM r WHERE r.TS = " + time }
results = list(client.QueryItems(collection_link, query, {"enableScanInQuery" : True}))


a = bytearray()
for doc in results:
    for b in base64.b64decode(doc["DataBlock"]["Samples"]):
       a.append(b)

d1 = (a.hex())[::2] 
d2 = (a.hex())[1::2] 
d3 = list(map(lambda s1, s2: s1+s2, d1, d2))

sup = []
for x in d3:
   sup.append(int(x, 16))

graf = plt.plot(sup)
yes =  plt.show(graf)
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Обработка данных форм</title>
        </head>
        <body>""")


print("<div>{}</div>".format(yes))

print("""</body>
        </html>""")


#date =  datetime.strptime(input("time: "),"%d.%m.%Y %H:%M:%S")
#wrongtime = str(time.mktime(date.timetuple()))
#time = wrongtime.replace(".0", "")
#print(time)        
