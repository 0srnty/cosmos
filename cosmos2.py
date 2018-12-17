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
time2 = form.getfirst("TEXT_1", "не задано")
date =  datetime.strptime(time2,"%Y-%m-%d")
wrongtime = str(time.mktime(date.timetuple()))
time1 = wrongtime.replace(".0", "")
config = {
'ENDPOINT':
    'PRIMARYKEY':
      'DATABASE':
    'CONTAINER':
}

client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={'masterKey': config['PRIMARYKEY']})
database_link = 'dbs/' + config['DATABASE']
db=client.ReadDatabase(database_link)
id= config['CONTAINER']
collection_link = database_link + '/colls/{0}'.format(id)
collection = client.ReadContainer(collection_link)
query =  { "query": "SELECT * FROM r WHERE r.TS >={} and r.TS<={}+86399 " .format(time1, time1) }
results = list(client.QueryItems(collection_link, query, {"enableScanInQuery" : True}))


a = []
for doc in results:
    if doc["TS"] not in a: 
       a.append(doc["TS"])
a1=[]                          
for i in a:
    a1.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)))

with open('text1.txt', 'w') as filehandle:
    for listitem in a1:
        filehandle.write('%s\n' % listitem)
        
filevar = open("text2.txt", 'w')
filevar.write(time2)
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
<input type="date" name="TEXT_1" value="{}">""".format(time2))
print("""
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
        
      </div>
    </div>

  </div>

</body>

</html>""")

