#!/usr/bin/env python3

# convert Freetaps point into gps file

from lxml import etree
import json
import urllib.request 

#https://api.freetaps.earth/waterpoints?format=xml
#https://api.freetaps.earth/waterpoints?format=json 
response = urllib.request.urlopen( "https://api.freetaps.earth/waterpoints?format=json" ) 
data = response.read()
encoding = response.info().get_content_charset('utf-8')
#jsonFreeTaps = {
#	"status": "Success",
#	"message": "Retrieved 12556 water points.",
#	"waterpoints": [{
#		"location": {
#			"latitude": 48.9030354,
#			"longitude": 2.4580216
#		},
#		"source": "osm",
#		"type": "FOUNTAIN"
#	},
#	{
#		"location": {
#			"latitude": 48.609402,
#			"longitude": 2.319922
#		},
#		"source": "manual_batch",
#		"type": "FOUNTAIN"
#	},
#	{
#		"location": {
#			"latitude": 0.098101,
#			"longitude": 0.198784
#		},
#		"source": "manual",
#		"type": "FOUNTAIN"
#	}]
#	}
#fileFreeTaps = open('waterpoints.json')
#jsonFreeTaps = json.load(fileFreeTaps)

jsonFreeTaps = json.loads(data.decode(encoding))


root_elem = etree.Element('gpx', version="1.1")
wp_processed = 0
for wp in jsonFreeTaps.get('waterpoints'):
	#print(i.get("location"))
	wpt_elem = etree.SubElement(root_elem, 'wpt')
	wpt_elem.set("lat", str(wp.get('location').get('latitude')))
	wpt_elem.set("lon", str(wp.get('location').get('longitude')))
	src_elem = etree.SubElement(wpt_elem, 'src')
	src_elem.text = wp.get('source')
	cmt_elem = etree.SubElement(wpt_elem, 'cmt')
	cmt_elem.text = wp.get('type')
	wp_processed += 1

#fileFreeTaps.close()

print(jsonFreeTaps.get('message'))
print(str(wp_processed) + " wp processed")
#print(etree.tostring(root_elem, pretty_print=True).decode("utf-8"))
tree = etree.ElementTree(root_elem)
tree.write('FreeTaps.gpx', pretty_print=True)
