This document describes the workflow of how to import the GEBADR list from the canton of Bern into OpenStreetMap in JOSM. The instruction is copied from the wiki.openstreetmap.org entry. A video tutorial is also available. The tasking manager is used for controlling and also an alternative way of mapping.
Wiki.openstreetmap entry: http://wiki.openstreetmap.org/wiki/Canton_of_Bern_Address_Import
Video tutorial: https://www.youtube.com/watch?v=pieUZrhfOdc&feature=youtu.be
Tasking manager: http://tasks.osmcanada.ca/project/48
by Stefan Berger (User:YBJazzer)
22.11.2016


Data Transformation

First, the data file in .dbf format is opened in a spreadsheet (e. g. Microsoft Excel) and saved as .csv file.

Information for LibreOffice and OpenOffice users
If you save the GEBADR_GADR.dbf file in your spreadsheet as .csv, two minor changes have to be made:
1. Change the delimiter in Script 1 from ";" to ",".
2. The entries of the first line of a .dbf file (which are the headers) look a bit special when opened in LibreOffice or OpenOffice spreadsheet.
They look like this: "LOKALISAT,C,60","GEBNR,C,12","BFSNR,N,4,0"
Change them manually to look like this: "LOKALISAT","GEBNR","BFSNR" or LOKALISAT,GEBNR,BFSNR

Data are then edited with two Python 3 scripts:

- Script 1 (before manual editing) creates three consecutive files: 
GEBADR_WGS84.csv - Reduces GEBADR list and adds WGS84 coordinates (calculated from Swiss coordinates LV95). 
GEBADR_OSMstyle.csv - Headers are changed to OSM keys and NUTZUNG entries are categorised into key:building. 
GEBADR_OSMstyle_edited.csv - Entries without housenumbers ("nn") and/or NUTZUNG "unterirdisches gebaeude" (underground building) are sorted out. 

The GEBADR_OSMstyle_edited.csv file is opened in a spreadsheet and edited manually. The addresses for import are selected and checked. The selection is saved as GEBADR_selection.csv. 

- Script 2 (after manual editing) creates a new file GEBADR_OSMimport.csv which has quotation marks added to all non-coordinate entries in the GEBADR_selection.csv. 
The created GEBADR_OSMimport.csv file can be easily imported to JOSM by the plug-in OpenData. 
The building nodes are merged to building polygons by using the plug-in Conflation. 

Changeset Tags
The changeset tags should contain the following information: 
Comment: "City: Street1 or Place1, Street2/Place2, ..."; e.g. "Bern: Ostring, Papiermühlestrasse, Pappelweg" 
Source: "Gebäudeadressen des Kantons Bern © Amt für Geoinformation des Kantons Bern"
Description: "https://wiki.openstreetmap.org/wiki/Canton_of_Bern_Address_Import"


Step by step instructions (English)
This instruction describes the edit of GEBADR data with Python 3 and Microsoft Excel spreadsheet. MS Excel will save .csv files with ";" as delimiter in German versions. The import plug-in OpenData will also use ";" as delimiter.
You need: Python 3 (to run the scripts with IDLE), a text editor (e.g. Notepad++) and a spreadsheet (e.g. Microsoft Excel). 
A video tutorial is available here [see link above].

Information for LibreOffice and OpenOffice users
If you save the GEBADR_GADR.dbf file in your spreadsheet as .csv, two minor changes have to be made:
- Change the delimiter in Script 1 from ";" to ",".
- The entries of the first line of a .dbf file (which are the headers) look a bit special when opened in LibreOffice or OpenOffice spreadsheet.
They look like this: "LOKALISAT,C,60","GEBNR,C,12","BFSNR,N,4,0"
Change them manually to look like this: "LOKALISAT","GEBNR","BFSNR" or LOKALISAT,GEBNR,BFSNR 

1. Download and unzip GEBADR.zip file. 
2. Open "...GEBADR/GEBADR/LV95/data/GEBADR_GADR.dbf" in a spreadsheet. 
3. Save as ".../GEBADR_GADR.csv" (MS-DOS) - This is important for correct display of umlauts and French letters. Check in a text editor whether umlauts are displayed correctly. 
4. Adjust Script 1: set input (".../GEBADR_GADR.csv") and output paths. Run the script. It will create three files as described above. 
Now some manual editing follows: 
5. Import ".../GEBADR_OSMstyle_edited.csv" to a spreadsheet (in Microsoft Excel: import as text, separate with ";", make sure each column is imported as text, not standard). Check if umlauts and coordinates are correctly displayed. 
6. Filter the addresses you want to import (with Pivot filter), check whether key:place should be used instead of key:street, and add street:fr (resp. place:fr) if necessary. Save file as ".../GEBADR_selection.csv" (Trennzeichen-getrennt). Check in a text editor if file contains your selection. 
7. Adjust Script 2, set input path ".../GEBADR_selection.csv" and output path. This script will add quotation marks to all non-coordinate entries, which is the format needed for import. 
8. Drag and drop ".../GEBADR_OSMimport.csv" into JOSM. The plug-in OpenData must be installed. 
9. Check whether nodes fit to buildings on aerial imagery. Preferrably, merge building nodes to building polygons using the plug-in Conflation. Otherwise, copy address nodes to the data layer using Ctrl+Shift+M. If you feel not sure about an address localisation, don't import it.
Previously mapped exact address nodes that represent entrances (e.g. Länggasse, Bern) can remain unchanged.
Addresses without buildings: Draw the building outline according to aerial imagery and merge address on building outline.
Multiple addresses in one building: Divide the building with new outlines and merge addresses on building part outlines. If you cannot do that, transfer building type to building polygon and delete key:building in address nodes.
10. Upload your data and cite source in changeset: 
Comment: "City: Street1, Street2, Street3" 
Source: "Gebäudeadressen des Kantons Bern © Amt für Geoinformation des Kantons Bern"
Description: "https://wiki.openstreetmap.org/wiki/Canton_of_Bern_Address_Import"



Step by step instructions (German)
Dies Anleitung beschreibt die Bearbeitung der GEBADR Daten mit Python 3 und dem Tabellenkalkulationsprogramm Microsoft Excel. MS Excel speichert Tabellen im .csv Format mit ";" als Delimiter. Das Import Plug-in OpenData benötigt ebenfalls ";" als Delimiter. Beachte dies (und korrigiere im Script) falls ein anderes Tabellenkalkulationsprogramm (z.B. Appache OpenOffice Calc) verwendet wird. 
Benötigt werden: Python 3 (um die Scripts mit IDLE laufen zu lassen), ein Texteditor (z.B. Notepad++) und ein Tabellenkalkulationsprogramm (z.B. Microsoft Excel). 
Ein Videotutorial findet sich hier [siehe Link oben].
 
Information für LibreOffice und OpenOffice Benutzer
Wenn du das GEBADR_GADR.dbf File im Tabellenkalkulationsprogramm als .csv speicherst, müssen zwei kleine Änderungen gemacht werden:
- Ändere den Delimiter in Script 1 von ";" zu ",".
- Die Einträge der ersten Zeile eines .dbf Files (was den Kategorietiteln entspricht) sehen etwas speziell aus im LibreOffice oder OpenOffice Tabellenkalkulationsprogramm.
Sie sehen folgendermassen aus: "LOKALISAT,C,60","GEBNR,C,12","BFSNR,N,4,0"
Ändere dies manuell zu: "LOKALISAT","GEBNR","BFSNR" oder LOKALISAT,GEBNR,BFSNR

1. Runterladen und entzippen der GEBADR.zip Datei. 
2. Öffne "...GEBADR/GEBADR/LV95/data/GEBADR_GADR.dbf" im Tabellenkalkulationsprogramm. 
3. Speichere als ".../GEBADR_GADR.csv" (MS-DOS) - Dies ist notwendig für die korrekte Darstellung von Umlauten und französischen Buchstaben, überprüfe im Texteditor die korrekte Schreibweise. 
4. Passe in Script 1 den input-Pfad ( ".../GEBADR_GADR.csv") und die output-Pfade an. Lasse das Script laufen. Es werden drei Dateien erstellt, welche weiter oben beschrieben sind. 
Jetzt folgt etwas manuelle Bearbeitung: 
5. Importiere ".../GEBADR_OSMstyle_edited.csv" ins Tabellenkalkulationsprogramm (in MS Excel: importiere als Text, trenne mit ";", und stelle sicher dass sämtliche Spalten als Text importiert werden). Überprüfe die korrekte Darstellung der Einträge. 
6. Filtere die Adressen, welche du importieren möchtest (mit dem Pivot-Filter), überprüfe ob key:place besser passt als key:street und korrigiere gegebenenfalls. Falls vorhanden, schreibe die französischen Strassennamen in die Spalte street:fr. Speichere die Datei als ".../GEBADR_selection.csv" (Trennzeichen-getrennt). Überprüfe im Texteditor, ob deine Auswahl wie gewünscht gezeigt wird. 
7. Passe in Script 2 den input-Pfad ( ".../GEBADR_selection.csv") und den ouput-Pfad an. Das Script schreibt Anführungszeichen zu allen nicht-Koordinateneinträgen. Dies ist die richtige Darstellung für den Import. 
8. Klicke und ziehe die Datei ".../GEBADR_OSMimport.csv" in JOSM. Das Plug-in OpenData muss installiert sein. 
9. Überprüfe ob die Gebäude-/Adresspunkte mit den Luftbildern übereinstimmen. Übertrage die Gebäude-/Adresspunkte auf die Gebäudeumrisse mittels Conflation Plug-in. Sofern kein Gebäudeumriss vorhanden ist, kopiere den Gebäude-/Adresspunkt mittels Ctrl+Shift+M in die Datenebene. Falls du dir über eine Adresse unsicher bist, importiere sie im Zweifelsfall nicht.
Bereits exakt auf Eingänge gemappte Adresspunkte (z.B. Länggasse, Bern) können so belassen werden.
Adressen ohne Gebäudeumriss: Zeichne den Gebäudeumriss entsprechend den Luftbildern und merge die Adresse auf den Gebäudeumriss.
Mehrere Adressen in einem Gebäude: Unterteile das Gebäude und merge die Adressen mit den Umrissen der Gebäudeteile. Falls dies nicht möglich ist, übertrage den Gebäudetyp auf den Gebäudeumriss und entferne ihn von den Addresspunkten.
10. Lade die Änderungen hoch und schreibe im Changeset: 
Kommentar/comment: "Ort: Strasse1, Strasse2, Strasse3" 
Quelle/source: "Gebäudeadressen des Kantons Bern © Amt für Geoinformation des Kantons Bern"
Beschreibung/description: "https://wiki.openstreetmap.org/wiki/Canton_of_Bern_Address_Import"
