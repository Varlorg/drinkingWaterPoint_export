#!/usr/bin/env python3

# export Eaupotable.info points into gps file

from lxml import etree
import json
import urllib.request 

response = urllib.request.urlopen( "https://eaupotable.info/fr/markers" ) 
data = response.read()
encoding = response.info().get_content_charset('utf-8')

jsonEauPotable = json.loads(data.decode(encoding))

root_elem_gpx = etree.Element('gpx', version="1.1")
root_elem_kml = etree.Element('kml', version="1.1")

wp_processed = 0

for wp in jsonEauPotable:
	
	# GPX
	wpt_elem_gpx = etree.SubElement(root_elem_gpx, 'wpt')
	wpt_elem_gpx.set("lat", str(wp.get('lat')))
	wpt_elem_gpx.set("lon", str(wp.get('lng')))
	src_elem_gpx = etree.SubElement(wpt_elem_gpx, 'src')
	src_elem_gpx.text = wp.get('absolute_url')
	name_elem_gpx = etree.SubElement(wpt_elem_gpx, 'name')
	name_elem_gpx.text = wp.get('title')
	desc_elem_gpx = etree.SubElement(wpt_elem_gpx, 'desc')
	desc_elem_gpx.text = wp.get('address')

	# KML
	pm_elem_kml = etree.SubElement(root_elem_kml, 'Placemark')
	pt_elem_kml = etree.SubElement(pm_elem_kml, 'Point')
	cdt_elem_kml = etree.SubElement(pt_elem_kml, 'coordinates')
	cdt_elem_kml.text = str(wp.get('lat')) + "," +  str(wp.get('lng'))
	name_elem_kml = etree.SubElement(pm_elem_kml, 'name')
	name_elem_kml.text = wp.get('title')
	dsc_elem_kml = etree.SubElement(pm_elem_kml, 'description')
	dsc_elem_kml.text = wp.get('absolute_url')
	addr_elem_kml = etree.SubElement(pm_elem_kml, 'address')
	addr_elem_kml.text = wp.get('address')
	
	wp_processed += 1

print(str(wp_processed) + " wp processed")
#print(etree.tostring(root_elem_gpx, pretty_print=True).decode("utf-8"))
tree_gpx = etree.ElementTree(root_elem_gpx)
tree_kml = etree.ElementTree(root_elem_kml)
tree_gpx.write('eaupotable-info.gpx', pretty_print=True)
tree_kml.write('eaupotable-info.kml', pretty_print=True)
