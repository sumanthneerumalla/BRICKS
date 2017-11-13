import csv

# Number of districts to partition
NUM_DISTRICTS = 8

# Open CSV file that has all MD ZIP codes
data = open('data_filtered.csv', 'rt')

# Dictionary to store all of the ZIP codes as keys and boundary coordinates as values
# Key = String - ZIP code
# Value = String Array - List of coordinate boundaries
zips = {}

# Dictionary to store all of the ZIP codes as keys and their neighboring ZIP codes as values
# Key = String - ZIP code
# Value = String Array - List of neighboring ZIP codes
neighbors = {}

# Keep track of the overall population
total_population = 0

# Read in all of the ZIP codes and their boundaries
for row in csv.reader(data):
	coordinates = row[8]
	cord_list = coordinates.split(' ')
	zips[row[1]] = cord_list
	total_population += row[3]

# Store the number of people that should be in each district
district_population = total_population / NUM_DISTRICTS

# Iterate over the dictionary of ZIPs
for key, value in zips.items():

	neighbor_set = set()

	# Iterate over the dictionary of ZIPs
	for key2, value2 in zips.items():

		# If you're comparing the same zip code, skip it
		if key == key2:
			continue

		# Iterate over the first list of coordinates
		for item in value:

			# Iterate over the second list of coordinates
			for item2 in value2:

				# If the coordinates are the same, the ZIPs are neighbors
				if item == item2:
					neighbor_set.add(key2)

	neighbors[key] = neighbor_set

for key, value in neighbors.items():
	print(key, ':', value)



class Zip:
	def __init__(self, name, neighbors):
		self.name = name
		self.neighbors = neighbors
		self.taken = false

class District:
	def __init__(self, number):
		self.number = number
		self.zips = Set()

	def addZip(self, zip):
		self.zips.add(zip)
