#!/usr/bin/env python3
import azure.cosmos.cosmos_client as cosmos_client
import json
import base64
from array import array
import binascii
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime
import site
import cgi
import html
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
form = cgi.FieldStorage()
time2 = form.getfirst("TEXT_2", "не задано")
date =  datetime.strptime(time2,"%Y-%m-%d %H:%M:%S")
wrongtime = str(time.mktime(date.timetuple()))
time1 = wrongtime.replace(".0", "")
config = {
    'ENDPOINT': 'https://ibecomfreecosmosdb.documents.azure.com:443',
    'PRIMARYKEY': 'wED2JFjQuXwJhl1UVuIWTmdKanpCr1vPA3uyp7hGJE81H0leAbSnhCZyMy5U0hCuJ85be4uQLZUyNttg5dWlWQ==',
    'DATABASE': 'vibromaketdb',
    'CONTAINER': 'vibromaketcol'
}

client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={'masterKey': config['PRIMARYKEY']})
database_link = 'dbs/' + config['DATABASE']
db=client.ReadDatabase(database_link)
id= config['CONTAINER']
collection_link = database_link + '/colls/{0}'.format(id)
collection = client.ReadContainer(collection_link)
query =  { "query": "SELECT * FROM r WHERE r.TS = " + time1 }
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
graf2 = plt.savefig('1.png')

a1=[]
with open('text1.txt', 'r') as filehandle:
    for line in filehandle:
        x = line[:-1]
        a1.append(x)
f = open("text2.txt")
fd = f.read()
print("Content-type: text/html\n")
print("""<!DOCTYPE html>
<html lang="ru">

<head>
  <meta charset="utf-8">
  <title>ibecom</title>
  <link href="http://40.113.78.202:8000/cosmos_site_css.css" rel ="stylesheet">
</head>

<body>
  <header>
    diagnostic equipment managment system
  </header>
  <div class="divall">

    <div class="div1">
      <ul>
        <li><a href="">Monitoring</a></li>
        <li><a href="">vibrodiagnostic</a></li>
        <li><a href="">servise</a></li>
      </ul>
    </div>
    <div class="div2">
<form action="/cgi-bin/cosmos2.py">
<input type="date" name="TEXT_1" value="{}">""".format(fd))
print(""">
<input type="submit">
</form>
<form action="/cgi-bin/cosmos.py">
<select name="TEXT_2">""")
for s in a1:
    print("""<option value="{}">{}</option>""".format(s, s[11:]))
print("""
<input type="submit">
</form>
      <div class="inner">
        <img src="http://40.113.78.202:8000/1.png">
      </div>
    </div>

  </div>

</body>

</html>""")
     
