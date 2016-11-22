# GEBADR_OSMimport_script2_selection_to_import.py
# Python 3 script that reads the '.../GEBADR_selection.csv' file and creates '.../GEBADR_OSMimport.csv' to import an address list by JOSM plug-in 'OpenData'.
# The script adds '"' to all non-coordinate entries. This is the style required by JOSM plug-in 'OpenData'.
# Stefan Berger (stefanberger.bscyb@gmx.ch)
# Updated 22 nov 2016

# SET YOUR INDIVIDUAL SETTINGS HERE:
inputfile_GEBADR_selection = '/Users/Stefan Berger/Desktop/GEBADR_selection.csv'
outputfile_GEBADR_OSMimport = '/Users/Stefan Berger/Desktop/GEBADR_OSMimport.csv'
set_delimiter = ';'
set_newline = ''

import csv
gebadr = open (inputfile_GEBADR_selection,'r', newline=set_newline)
gebadr_read = csv.DictReader(gebadr, delimiter=set_delimiter)
data = {}
for row in gebadr_read:
	for header, value in row.items():
		try:
			data[header].append(value)
		except KeyError:
			data[header] = [value]

addr_country = data['addr:country']
addr_postcode = data['addr:postcode']
addr_city = data['addr:city']
addr_street = data['addr:street']
addr_street_fr = data['addr:street:fr']
addr_place = data['addr:place']
addr_place_fr = data['addr:place:fr']
addr_housenumber = data['addr:housenumber']
building = data['building']
ele = data['ele']
latitude_strings = data['latitude']
latitude = [float(i) for i in latitude_strings]
longitude_strings = data['longitude']
longitude = [float(i) for i in longitude_strings]

with open('/Users/Stefan Berger/Desktop/GEBADR_OSMimport.csv', 'w', newline=set_newline, encoding='utf-8') as new_file_with_wgs84_coordinates:
	writer = csv.writer(new_file_with_wgs84_coordinates, delimiter=set_delimiter, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(['addr:country', 'addr:postcode','addr:city', 'addr:street', 'addr:street:fr', 'addr:place', 'addr:place:fr', 'addr:housenumber', 'building', 'ele', 'latitude', 'longitude'])		
with open('/Users/Stefan Berger/Desktop/GEBADR_OSMimport.csv', 'a', newline=set_newline, encoding='utf-8') as new_file_with_wgs84_coordinates:
	writer = csv.writer(new_file_with_wgs84_coordinates, delimiter=set_delimiter, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerows(zip(addr_country, addr_postcode, addr_city, addr_street, addr_street_fr, addr_place, addr_place_fr, addr_housenumber, building, ele, latitude, longitude))