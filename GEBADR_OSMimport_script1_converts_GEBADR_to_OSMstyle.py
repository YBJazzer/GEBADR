#  GEBADR_OSMimport_script1_converts_GEBADR_to_OSMstyle.py
#  Python 3 script that transforms the GEBADR address list from the canton of Bern into an OpenStreetMap style address list.
    
#  This script uses the calculation from a coordinate transformation script by swisstopo:

#  #####
#  The MIT License (MIT)
  
#  Copyright (c) 2014 Federal Office of Topography swisstopo, Wabern, CH and Aaron Schmocker 
  
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#  
#  The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.

# Information about the original swisstopo script (WGS84 <-> LV03 converter)
# WGS84 <-> LV03 converter for Python 2
# Aaron Schmocker [aaron@duckpond.ch]
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab

# Source: http://www.swisstopo.admin.ch/internet/swisstopo/en/home/topics/survey/sys/refsys/projections.html (see PDFs under "Documentation")
# Updated 9 dec 2014
# Please validate your results with NAVREF on-line service: http://www.swisstopo.admin.ch/internet/swisstopo/en/home/apps/calc/navref.html (difference ~ 1-2m)
# #####


# This script is an extension of the above described original script. It calculates the transfomation LV95 -> WGS84 for a list in .csv format.
# Important changes to original version: Input LV95 instead of LV03, reduced to monodirectional LV95 -> WGS84 converter, input coordinates from .csv file (delimiter for separating data items ";"), script for Python 3.
# The coordinate transformation calculation is unchanged from the original swisstopo script.
# The script calculates through the GEBADR_GADR list from the canton of Bern. The list is available here: http://www.apps.be.ch/geo/index.php?tmpl=index&option=com_easysdi_catalog&Itemid=2&context=geocatalog&toolbar=1&task=showMetadata&type=complete&id=5dfcc475-ef53-4483-a7f0-5d8e503fea9f&lang=de
# Open the ".../GEBADR/LV95/data/GEBADR_GADR.dbf" file in Excel and save as .csv (MS-DOS). In Excel, the delimiter for data items in .csv files is set as ";" by default.
# Run this script. Three outputfiles are created:
# Outputfile GEBADR_WGS84: '.../GEBADR_WGS84.csv' contains two aditional columns for WGS84 latitude and longitude and misses some columns that are not relevant for further use in OSM.
# Outputfile GEBADR_OSMstyle: '.../GEBADR_OSMstyle.csv' has headers changed to OSM keys and the NUTZUNG entries are categorised into OSM key:building tags.
# Outputfile GEBADR_OSMstyle_edited: '.../GEBADR_OSMstyle_edited.csv' is filtered out by adresses that have no housenumber ('nn') and the NUTZUNG tag 'unterirdisches gebaeude' (= underground building).
# Updated 22 nov 2016
# Stefan Berger (stefanberger.bscyb@gmx.ch)

# SET YOUR INDIVIDUAL SETTINGS HERE:
inputfile_GEBADR_GADR = '/Users/Stefan Berger/Desktop/GEBADR_GADR.csv'
outputfile_GEBADR_WGS84 = '/Users/Stefan Berger/Desktop/GEBADR_WGS84.csv'
outputfile_GEBADR_OSMstyle = '/Users/Stefan Berger/Desktop/GEBADR_OSMstyle.csv'
outputfile_GEBADR_OSMstyle_edited = '/Users/Stefan Berger/Desktop/GEBADR_OSMstyle_edited.csv'
set_delimiter = ';'
set_newline = ''


# Opens '.../GEBADR_GADR.csv' file.
# Reads columns GROBKOOR_E and GROBKOOR_N and creates list.

import csv
gebadr = open (inputfile_GEBADR_GADR,'r', newline=set_newline)
gebadr_read = csv.DictReader(gebadr, delimiter=set_delimiter)
data = {}
for row in gebadr_read:
	for header, value in row.items():
		try:
			data[header].append(value)
		except KeyError:
			data[header] = [value]

ch_east  = data['GROBKOOR_E']
ch_north = data['GROBKOOR_N']

# Changes strings to integers.
ch_east_integers  = list(map(int, ch_east))
ch_north_integers = list(map(int, ch_north))

# Creates a list of 2D matrices of each associated north and east coordinate.
coordinates = [list(a) for a in zip(ch_east_integers, ch_north_integers)]

# Calculates LV95 to WGS84 (adapted from original script).
wgs84_list = []
for lv95 in coordinates:

	import math

	class GPSConverter(object):
		'''
		GPS Converter class which is able to perform convertions from CH1903+ and WGS84 system.
		'''

		# Convert CH y/x to WGS lat
		def CHtoWGSlat(self, y, x):
			# Axiliary values (% Bern)
			y_aux = (y - 2600000) / 1000000
			x_aux = (x - 1200000) / 1000000
			lat = (16.9023892 + (3.238272 * x_aux)) + \
					- (0.270978 * pow(y_aux, 2)) + \
					- (0.002528 * pow(x_aux, 2)) + \
					- (0.0447 * pow(y_aux, 2) * x_aux) + \
					- (0.0140 * pow(x_aux, 3))
			# Unit 10000" to 1" and convert seconds to degrees (dec)
			lat = (lat * 100) / 36
			return lat

		# Convert CH y/x to WGS long
		def CHtoWGSlng(self, y, x):
			# Axiliary values (% Bern)
			y_aux = (y - 2600000) / 1000000
			x_aux = (x - 1200000) / 1000000
			lng = (2.6779094 + (4.728982 * y_aux) + \
					+ (0.791484 * y_aux * x_aux) + \
					+ (0.1306 * y_aux * pow(x_aux, 2))) + \
					- (0.0436 * pow(y_aux, 3))
			# Unit 10000" to 1" and convert seconds to degrees (dec)
			lng = (lng * 100) / 36
			return lng

		# Convert decimal angle (° dec) to sexagesimal angle (dd.mmss,ss)
		def DecToSexAngle(self, dec):
			degree = int(math.floor(dec))
			minute = int(math.floor((dec - degree) * 60))
			second = (((dec - degree) * 60) - minute) * 60
			return degree + (float(minute) / 100) + (second / 10000)
			
		# Convert sexagesimal angle (dd.mmss,ss) to seconds
		def SexAngleToSeconds(self, dms):
			degree = 0 
			minute = 0 
			second = 0
			degree = math.floor(dms)
			minute = math.floor((dms - degree) * 100)
			second = (((dms - degree) * 100) - minute) * 100
			return second + (minute * 60) + (degree * 3600)

		# Convert sexagesimal angle (dd.mmss) to decimal angle (degrees)
		def SexToDecAngle(self, dms):
			degree = 0
			minute = 0
			second = 0
			degree = math.floor(dms)
			minute = math.floor((dms - degree) * 100)
			second = (((dms - degree) * 100) - minute) * 100
			return degree + (minute / 60) + (second / 3600)
		
		def LV95toWGS84(self, east, north):
			'''
			Convert LV95 to WGS84 Return a array of double that contain lat and long
			'''
			d = []
			d.append(self.CHtoWGSlat(east, north))
			d.append(self.CHtoWGSlng(east, north))
			return d

	if __name__ == "__main__":
		''' Example usage for the GPSConverter class.'''
		
		converter = GPSConverter()

		# Convert LV95 to WGS84 coordinates
		wgs84 = converter.LV95toWGS84(lv95[0], lv95[1])
	
	wgs84_list += [wgs84]

# Creates two lists for WGS84 latitude and WGS84 longitude.
wgs84_list_lat_and_list_long = list(map(list, zip(*wgs84_list))) 
wgs84_latitude_integers   = wgs84_list_lat_and_list_long[0]
wgs84_longitude_integers  = wgs84_list_lat_and_list_long[1]

# Writes a new '.../GEBADR_WGS84.csv' file containing two new columns for WGS84 latitude and WGS84 longitude.
gebadr = open (inputfile_GEBADR_GADR,'r', newline=set_newline)
gebadr_read = csv.DictReader(gebadr, delimiter=set_delimiter)
data = {}
for row in gebadr_read:
	for header, value in row.items():
		try:
			data[header].append(value)
		except KeyError:
			data[header] = [value]

plz_strings = data['PLZ']
ort = data['ORT']
lokalisat = data['LOKALISAT']
gebnr = data['GEBNR']
nutzung = data['NUTZUNG']
hoehe_strings = data['HOEHE']
grobkoor_e_strings  = data['GROBKOOR_E']
grobkoor_n_strings = data['GROBKOOR_N']

plz = list(map(int, plz_strings))
hoehe = list(map(int, hoehe_strings))
grobkoor_e = list(map(int, grobkoor_e_strings))
grobkoor_n = list(map(int, grobkoor_n_strings))
wgs84_lat = wgs84_latitude_integers
wgs84_long = wgs84_longitude_integers

with open(outputfile_GEBADR_WGS84, 'w', newline=set_newline) as new_file_with_wgs84_coordinates:
	writer = csv.writer(new_file_with_wgs84_coordinates, delimiter=set_delimiter)
	writer.writerow(['PLZ','ORT', 'LOKALISAT', 'GEBNR', 'NUTZUNG', 'HOEHE', 'GROBKOOR_E', 'GROBKOOR_N', 'WGS84_LAT', 'WGS84_LONG'])		
with open(outputfile_GEBADR_WGS84, 'a', newline=set_newline) as new_file_with_wgs84_coordinates:
			writer = csv.writer(new_file_with_wgs84_coordinates, delimiter=set_delimiter)
			writer.writerows(zip(plz, ort, lokalisat, gebnr, nutzung, hoehe, grobkoor_e, grobkoor_n, wgs84_lat, wgs84_long))
			
			
# This part converts the GEBADR_WGS84.csv file into an OpenStreetMap-suitable style.
# After running, edit, check and select the desired address data ('.../GEBADR_OSMstyle_edited.csv') in a spreadsheet (e.g. Microsoft Excel) and save as '.../Desktop/GEBADR_selection.csv' (Trennzeichen-getrennt).

# Opens GEBADR_WGS84.csv file and reads all columns.
import csv
gebadr = open (outputfile_GEBADR_WGS84,'r', newline=set_newline)
gebadr_reader = csv.DictReader(gebadr, delimiter=set_delimiter)
data = {}
for row in gebadr_reader:
	for header, value in row.items():
		try:
			data[header].append(value)
		except KeyError:
			data[header] = [value]

addr_postcode = data['PLZ']
addr_country = ['CH']*len(addr_postcode) # Creates a column with 'CH' entries.
addr_city = data['ORT']
addr_city = [element.replace('b.', 'bei') for element in addr_city] # Replaces the abbreviation 'b.' with 'bei' in city/village names.
addr_street = data['LOKALISAT']
addr_street_fr = ['']*len(addr_street) # Creates an empty column for french street names.
addr_place = ['']*len(addr_street) # Creates an empty column for place names.
addr_place_fr = ['']*len(addr_street) # Creates an empty column for french place names.
addr_housenumber = data['GEBNR']
building = data['NUTZUNG']

# The following lines replace German terms from the NUTZUNG column in the GEBADR list by OpenStreetMap keys for buildings. All unspecified buildings receive the expression 'yes'.
building = ['residential' if (x=='Wohnhaus' or x=='Ferienhaus' or x=='Wohnstock' or x=='Wohnhaus/Werkstatt' or x=='Wohnhaus/Atelier' or x=='Wohnhaus/Garage' or x=='Terrassenhaus' or x=='Ferienheim' or x=='Chalet' or x=='Wohnhaus/Post') else x for x in building]
building = ['garage' if (x=='Garage' or x=='Garage/Werktstatt' or x=='Garage/Schopf' or x=='Garage/Lager' or x=='Garage/Remise' or x=='Garage/Sitzplatz' or x=='Werkstatt/Garage' or x=='Garage/Einstellraum') else x for x in building]
building = ['barn' if (x=='Scheune' or x=='Schopf' or x=='Speicher' or x=='Heuhaus' or x=='Scheune/Weidhaus' or x=='Holzschopf' or x=='Wagenschopf' or x=='Schopf/Garage' or x=='Lagerschopf' or x=='Schopf/Stall') else x for x in building]
building = ['farm' if (x=='Wohnhaus/Scheune' or x=='Bauernhaus' or x=='Bauernhaus Wohnhaus/Scheune' or x=='Wohnhaus/Stall' or x=='Scheune Wohnhaus') else x for x in building]
building = ['house' if (x=='Wohn- und Geschäftshaus' or x=='Wohnnhaus/Gewerbe' or x=='Restaurant Wohn- und Geschäftshaus') else x for x in building]
building = ['shed' if (x=='Einstellraum' or x=='Gartenhaus' or x=='Gerätehaus' or x=='Geräteschuppen') else x for x in building]
building = ['roof' if (x=='Autounterstand' or x=='unterstand' or x=='Unterstand' or x=='Velounterstand' or x=='Tankstelle' or x=='Brunnenscherm' or x=='Veloscherm') else x for x in building]
building = ['farm_auxiliary' if (x=='Hühnerhaus' or x=='Stall' or x=='Silo' or x=='Schafstall' or x=='Geflügelmasthalle' or x=='Laufstall' or x=='Geflügelhalle' or x=='Boxenlaufstall' or x=='Masthalle') else x for x in building]
building = ['commercial' if (x=='Geschäftshaus' or x=='Bürogebäude' or x=='Gewerbebetrieb' or x=='Gewerbehaus') else x for x in building]
building = ['sty' if (x=='Schweinescheune' or x=='Schweinestall') else x for x in building]
building = ['cabin' if (x=='Sennhütte' or x=='Weidhaus' or x=='Alphütte' or x=='Finel' or x=='Weidhaus/Scheune' or x=='Waldhütte' or x=='Forsthaus' or x=='Heufinel' or x=='Heuhütte' or x=='Alpstall' or x=='Hütte' or x=='Schutzhütte' or x=='Waldhaus' or x=='Alpgebäude') else x for x in building]
building = ['service' if (x=='Trafostation' or x=='reservoir' or x=='Pumpwerk' or x=='Pumpstation' or x=='Pumpstation') else x for x in building]
building = ['school' if (x=='Schulhaus' or x=='Schulpavillon') else x for x in building]
building = ['warehouse' if (x=='Magazin' or x=='Lagerhalle' or x=='Lagerhaus') else x for x in building]
building = ['industrial' if (x=='Fabrik') else x for x in building]
building = ['greenhouse' if (x=='Gewächshaus' or x=='Treibhaus') else x for x in building]
building = ['stable' if (x=='Pferdestall') else x for x in building]
building = ['church' if (x=='Kirche') else x for x in building]
building = ['garages' if (x=='Garages' or x=='Garagen') else x for x in building]
building = ['hotel' if (x=='Hotel') else x for x in building]
building = ['kiosk' if (x=='Kiosk') else x for x in building]
building = ['chapel' if (x=='Kapelle') else x for x in building]
building = ['retail' if (x=='Laden') else x for x in building]
building = ['bridge' if (x=='bruecke passarelle') else x for x in building]
building = ['yes' if not (x=='residential' or x=='garage' or x=='barn' or x=='farm' or x=='house' or x=='shed' or x=='roof' or x=='farm_auxiliary' or x=='commercial' or x=='sty' or x=='cabin' or x=='service' or x=='school' or x=='warehouse' or x=='industrial' or x=='greenhouse' or x=='stable' or x=='church' or x=='garages' or x=='hotel' or x=='kiosk' or x=='chapel' or x=='retail' or x=='bridge' or x=='unterirdisches gebaeude') else x for x in building]

ele = data['HOEHE']
ele = ['' if x=='0' else x for x in ele] # Replaces altitudes '0' by '' (empty entry, no key will be created in OSM).
latitude = data['WGS84_LAT']
longitude = data['WGS84_LONG']

# A new file is written containing the correct OSM keys as headers.
with open(outputfile_GEBADR_OSMstyle, 'w', newline=set_newline) as new_file_with_wgs84_coordinates:
	writer = csv.writer(new_file_with_wgs84_coordinates, delimiter=set_delimiter)
	writer.writerow(['addr:country', 'addr:postcode','addr:city', 'addr:street', 'addr:street:fr', 'addr:place', 'addr:place:fr', 'addr:housenumber', 'building', 'ele', 'latitude', 'longitude'])		
with open(outputfile_GEBADR_OSMstyle, 'a', newline=set_newline) as new_file_with_wgs84_coordinates:
	writer = csv.writer(new_file_with_wgs84_coordinates, delimiter=set_delimiter)
	writer.writerows(zip(addr_country, addr_postcode, addr_city, addr_street, addr_street_fr, addr_place, addr_place_fr, addr_housenumber, building, ele, latitude, longitude))

# Adresses that have no housenumber ('nn') and the NUTZUNG tag 'unterirdisches gebaeude' (= underground building) are removed.			
with open(outputfile_GEBADR_OSMstyle, 'r', newline=set_newline) as delhousenr_nn_in, open(outputfile_GEBADR_OSMstyle_edited, 'w', newline=set_newline) as delhousenr_nn_out:
	writer = csv.writer(delhousenr_nn_out, delimiter=set_delimiter)
	for line in csv.reader(delhousenr_nn_in, delimiter=set_delimiter):
		if not 'nn' in line:
			if not 'unterirdisches gebaeude' in line:
						writer.writerow(line)