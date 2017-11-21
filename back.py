'''back.py'''
import csv

# State to district
STATE = 'MD'

# Number of districts to partition
NUM_DISTRICTS = 8

# Dictionary to store all of the ZIP codes as keys and their populations as values
# Key = String - ZIP code
# Value = Int - Population of ZIP code
pops = {}

# Dictionary to store all of the ZIP codes as keys and boundary coordinates as values
# Key = String - ZIP code
# Value = String Array - List of coordinate boundaries
zips = {}

# Dictionary to store all of the ZIP codes as keys and their neighboring ZIP codes as values
# Key = String - ZIP code
# Value = String Array - List of neighboring ZIP codes
neighbors = {}

# Dictionary to store all of the districts and the zip codes within them
# Key = String - District name
# Value = String Array - List of zip codes in district
districts = {}

# Keep track of the overall population
total_population = 0

# Store the number of people that should be in each district
pop_per_district = 0


def taken(zip_code):
	''' Returns True if ZIP code is already taken by another district
		and False if the ZIP code is available '''

	for key, value in districts.items():
		if zip_code in value:
			return True

	return False


def read_data():
	''' Reads the data (ZIP codes, boundary coordinates, populations)
		into their corresponding data structures '''

	global total_population

	# Open CSV file that has all MD ZIP codes
	data = open('Data/data-filtered/data_filtered_' + STATE + '.csv', 'rt')

	# Read in all of the ZIP codes and their boundaries
	for row in csv.reader(data):
		coordinates = row[8]
		cord_list = coordinates.split(' ')
		zips[row[1]] = cord_list
		pops[row[1]] = int(row[3])
		total_population += int(row[3])


def find_neighbors():
	''' Iterates through all of the ZIP codes stores neighbors
		when two ZIP codes share a boundary '''

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


def create_districts():
	''' Creates contiguous districts of relatively equal size
		and stores them in a dictionary '''

	# Iterate over the districts
	for district, value1 in districts.items():
		current_pop = 0

		# Iterate over the neighbor dictionary
		for neighbor, value2 in neighbors.items():
			
			# Only add ZIP codes while the districts population is not high enough
			if current_pop < pop_per_district:

				# If the key ZIP code is not taken, add it to the district
				if not taken(neighbor):
					value1.add(neighbor)
					current_pop += pops[neighbor]

			# Iterate over the neighbors of the current ZIP
			for i in value2:

				# Only add ZIP codes while the districts population is not high enough
				if current_pop < pop_per_district:

					# If ZIP code is not taken, add it to the district
					if not taken(i):
						value1.add(i)
						current_pop += pops[i]


def print_dictionary(dictionary):
	''' Print out the passed in dictionary in the form:
		key : value '''
	values = 0

	for key, value in dictionary.items():
		print(key, ':', value)
		print()
		values += len(value)


def print_district_pops():
	''' Print out the population of each district '''
	sum = 0
	for key, value in districts.items():
		district_pop = 0

		for i in value:
			district_pop += pops.get(i)
			sum += pops.get(i)
		print(key, 'population:', district_pop)

	print("Sum:", sum)

# Read in data from input file
read_data()

pop_per_district = total_population / NUM_DISTRICTS

# Find all of the neighbors of each ZIP code
find_neighbors()

# Fill dictionary with correct number of districts and empty zip code list
for x in range(NUM_DISTRICTS):
	districts['District ' + str(x+1)] = set()

# Create the districts
create_districts()

print_dictionary(districts)

print_district_pops()

'''
file2 = open('output.txt', 'wt')

for dist11, zip11 in districts.items():

	string1 = 'path: ['
	string2 = 'new google.maps.LatLng('

	for x in zip11:
		for key2, value2 in zips.items():
			if x == key2: 
				for i in value2:
					crd_lst = i.split(',')
					new_str = string2 + crd_lst[1] + ',' + crd_lst[0] + '),'
					string1 = string1 + new_str
	string1 += ']'
	print(string1)
	print()
	file2.write(string1)
	file2.write('\n')
	file2.write('\n')

file2.close()
'''

# Check to make sure sum of district populations equals the total population
print("Total population:", total_population)
