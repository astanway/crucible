# Grab a Graphite JSON formatted timeseries for use in Crucible
# usage: graphite-grab.py "http://graphite.etsycorp.com/render/?width=1400&from=-24hour&target=stats.timers.api.getPage.200.mean&format=json"
import json
import sys
import requests
import urlparse

url = sys.argv[1]
r = requests.get(url)
js = r.json()
datapoints = js[0]['datapoints']

converted = []
for datapoint in datapoints:
	new_datapoint = [datapoint[1], datapoint[0]]
	converted.append(new_datapoint)

parsed = urlparse.urlparse(url)
target = urlparse.parse_qs(parsed.query)['target'][0]
with open("data/" + target + '.json', 'w') as f:
    f.write(json.dumps(converted))
    f.close()
