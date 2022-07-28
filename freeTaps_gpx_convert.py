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

root_elem_gpx = etree.Element('gpx', version="1.1")
root_elem_kml = etree.Element('kml', version="1.1")

wp_processed = 0
for wp in jsonFreeTaps.get('waterpoints'):
	#print(i.get("location"))
	
	# GPX
	wpt_elem_gpx = etree.SubElement(root_elem_gpx, 'wpt')
	wpt_elem_gpx.set("lat", str(wp.get('location').get('latitude')))
	wpt_elem_gpx.set("lon", str(wp.get('location').get('longitude')))
	src_elem_gpx = etree.SubElement(wpt_elem_gpx, 'src')
	src_elem_gpx.text = wp.get('source')
	cmt_elem_gpx = etree.SubElement(wpt_elem_gpx, 'cmt')
	cmt_elem_gpx.text = wp.get('type')
	
	# KML
	pm_elem_kml = etree.SubElement(root_elem_kml, 'Placemark')
	pt_elem_kml = etree.SubElement(pm_elem_kml, 'Point')
	cdt_elem_kml = etree.SubElement(pt_elem_kml, 'coordinates')
	cdt_elem_kml.text = str(wp.get('location').get('latitude')) + "," +  str(wp.get('location').get('longitude'))
	dsc_elem_kml = etree.SubElement(pm_elem_kml, 'description')
	dsc_elem_kml.text = wp.get('type') + "\n" + wp.get('source')
	
	wp_processed += 1

#fileFreeTaps.close()

print(jsonFreeTaps.get('message'))
print(str(wp_processed) + " wp processed")
#print(etree.tostring(root_elem_gpx, pretty_print=True).decode("utf-8"))
tree_gpx = etree.ElementTree(root_elem_gpx)
tree_kml = etree.ElementTree(root_elem_kml)
tree_gpx.write('FreeTaps.gpx', pretty_print=True)
tree_kml.write('FreeTaps.kml', pretty_print=True)

