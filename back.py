import csv

data = open('data_filtered.csv', 'rt')

zips = {}

for row in csv.reader(data):

	coordinates = row[8]
	cord_list = coordinates.split(' ')
	zips[row[1]] = cords_list
