# Grab a Graphite JSON formatted timeseries for use in Crucible
# usage: graphite-grab.py "http://graphite.etsycorp.com/render/?width=1400&from=-24hour&target=stats.timers.api.getPage.200.mean&format=json"
import json
import sys
import requests
import urlparse
import os
from os.path import dirname, join, abspath

url = sys.argv[1]

if "&format=json" not in url:
	url += "&format=json"

r = requests.get(url)
js = r.json()
datapoints = js[0]['datapoints']

converted = []
for datapoint in datapoints:
    try:
    	new_datapoint = [float(datapoint[1]), float(datapoint[0])]
    	converted.append(new_datapoint)
    except:
        continue

parsed = urlparse.urlparse(url)
target = urlparse.parse_qs(parsed.query)['target'][0]

data_folder = abspath(join(dirname( __file__ ), '..', 'data'))

with open(data_folder + "/" + target + '.json', 'w') as f:
    f.write(json.dumps(converted))
    f.close()
