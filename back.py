import csv
from fastkml import kml

data = open('data_filtered.csv', 'rt')

neighbors = {}

for row1 in csv.reader(data):
	k = kml.KML()
	k.from_string(row1[11])
	
	root = parser.fromstring(row1[11])
	print(root.Polygon.outerBoundaryIs.LinearRing.coordinates.text)
	#for row2 in csv.reader(data):
			
