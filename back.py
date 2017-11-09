import csv

data = open('data_filtered.csv', 'rt')

zips = {}

for row in csv.reader(data):

	zips[row[1]] = row[9]
