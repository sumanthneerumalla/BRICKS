'''back.py'''
import csv
import copy
from geopy.distance import vincenty

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

# Dictionary to store all of the districts and their outlining boundary
# Key = String - District name
# Value = String Set - Set of coordinates in the boundary
district_boundary = {}

# Dictionary to store all of the ZIP codes as keys and the coordinates of their center point as values
# Key = String - ZIP code
# Value = Float Tuple - Pair of coordinates
centers = {}

# Keep track of the overall population
total_population = 0

# Store the number of people that should be in each district
pop_per_district = 0


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

		# Make sire there are no blank coordinates
		for item in cord_list:
			if item == '':
				cord_list.remove(item)

		zips[row[1]] = cord_list
		pops[row[1]] = int(row[3])
		center_tuple = (float(row[2]), float(row[6]))
		centers[row[1]] = center_tuple
		total_population += int(row[3])


def find_neighbors():
	''' Iterates through all of the ZIP codes stores neighbors
		when two ZIP codes share a boundary '''

	# Iterate over the dictionary of ZIPs
	for key, value in zips.items():
		neighbor_list = []

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

						# Don't add the same zips twice
						if key2 not in neighbor_list:
							neighbor_list.append(key2)

		neighbors[key] = neighbor_list


def find_closest_neighbor(zip_code, taken):
	'''Returns the closest zip code to the zip passed in that
		is not already taken'''

	potential_list = []
	zip_center = centers.get(zip_code)

	# Add all zip codes that are not taken to the potential list
	for item in centers.keys():
		if item not in taken and item != zip_code:
			potential_list.append(item)

	closest = potential_list[0]

	# Loop through the potential list and find the zip with the
	# smallest distance to our target zip code
	for item in potential_list:
		closest_center = centers.get(closest)
		test_center = centers.get(item)

		if vincenty(zip_center, closest_center).feet > vincenty(zip_center, test_center).feet:
			closest = item

	return closest


def create_districts(pop_per_district):
	''' Creates contiguous districts of relatively equal size
		and stores them in a dictionary '''

	current_neighbors = []
	taken = []
	district_list = []
	district_count = 1
	current_pop = 0
	first_iteration = True

	while len(taken) != len(zips.keys()):

		# If the current population becomes larger than the population per district,
		# save the current district and start the next one
		#print('Length of taken: ' + str(len(taken)))
		#print('Length of zips: ' + str(len(zips.keys())))
		if current_pop >= pop_per_district:
			districts['District ' + str(district_count)] = district_list
			district_list = []
			district_count += 1
			current_pop = 0
			current_zip = current_neighbors[0]
			current_neighbors = []

		if first_iteration:
			first_iteration = False
			current_zip = list(neighbors.keys())[0]
			district_list.append(current_zip)
			taken.append(current_zip)
			current_pop += pops.get(current_zip)
			n_list = neighbors.get(current_zip)

			for item in n_list:
				if item not in taken and item not in current_neighbors:
					current_neighbors.append(item)

		else:

			# If we're on the last zip code, add it to the last district and exit loop
			if len(taken) == len(zips.keys()) - 1:
				district_list.append(current_zip)
				current_pop += pops.get(current_zip)
				districts['District ' + str(district_count)] = district_list
				break

			if not current_neighbors:
				current_zip = find_closest_neighbor(current_zip, taken)
				district_list.append(current_zip)
				taken.append(current_zip)
				current_pop += pops.get(current_zip)
				n_list = neighbors.get(current_zip)

				for item in n_list:
					if item not in taken and item not in current_neighbors:
						current_neighbors.append(item)

			else:
				current_zip = current_neighbors[0]
				current_neighbors.remove(current_zip)
				district_list.append(current_zip)
				taken.append(current_zip)
				current_pop += pops.get(current_zip)
				n_list = neighbors.get(current_zip)

				for item in n_list:
					if item not in taken and item not in current_neighbors:
						current_neighbors.append(item)


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


def outline_districts():
	'''Union all of the zip code coordinate boundaries for
		each district to get only the outlining boundary'''

	# Iterate over the district dictionary
	for district, zip_codes in districts.items():

		current_boundary = []
		first_iteration = True

		for item in zip_codes:

			if first_iteration:
				first_iteration = False
				set1 = zips.get(item)
				for i in set1:
					current_boundary.append(i)
				continue

			set1 = zips.get(item)
			#print("Curent boundary before: " + str(current_boundary))
			current_boundary = set(current_boundary).symmetric_difference(set1)
			#print("Curent boundary after: " + str(current_boundary))
			#print()

		district_boundary[district] = current_boundary


def output_individuals():
	# Open output file for writing HTML script
	file2 = open('output.txt', 'wt')

	strokeColors = ['#FF0000', '#0078FF', '#663300', '#ffff00', '#009900', '#660066', '#ff9900', '#ff99ff']
	outerCount = 0
	innerCount = 0

	for dist11, zip11 in districts.items():

		string1 = '\tpath: ['
		string2 = 'new google.maps.LatLng('

		for x in zip11:

			stringBegin = 'var line' + str(innerCount) + ' = new google.maps.Polyline({\n'
			stringEnd = '\tstrokeColor: "' + str(strokeColors[outerCount]) + '",\n\tstrokeOpacity: 1.0,\n\tstrokeWeight: 2,\n\tmap: map\n});'

			for key2, value2 in zips.items():
				if x == key2:
					for i in value2:
						crd_lst = i.split(',')
						new_str = string2 + crd_lst[1] + ',' + crd_lst[0] + '),'
						string1 = string1 + new_str

			string1 = string1[:-1]
			string1 += '],\n'
			file2.write(stringBegin + string1 + stringEnd)
			file2.write('\n')
			file2.write('\n')

			string1 = 'path: ['
			innerCount += 1

		outerCount += 1

	file2.close()


def output_outlines():
	# Open output file for writing HTML script
	file2 = open('output_copy.txt', 'wt')

	strokeColors = ['#FF0000', '#0078FF', '#663300', '#ffff00', '#009900', '#660066', '#ff9900', '#ff99ff']
	count =  0

	for district, outline in district_boundary.items():

		string1 = '\tpath: ['
		string2 = 'new google.maps.LatLng('

		for x in outline:
			crd_lst = x.split(',')
			new_str = string2 + crd_lst[1] + ',' + crd_lst[0] + '),'
			string1 = string1 + new_str

		stringBegin = 'var line' + str(count) + ' = new google.maps.Polyline({\n'
		stringEnd = '\tstrokeColor: "' + str(strokeColors[count]) + '",\n\tstrokeOpacity: 1.0,\n\tstrokeWeight: 2,\n\tmap: map\n});'
		count += 1

		string1 = string1[:-1]
		string1 += '],\n'
		file2.write(stringBegin + string1 + stringEnd)
		file2.write('\n')
		file2.write('\n')

		string1 = 'path: ['

	file2.close()


def run(state, num_districts):
	'''Run the program'''
	
	STATE = state
	NUM_DISTRICTS = int(num_districts)

	# Read in data from input file
	read_data()

	pop_per_district = total_population / NUM_DISTRICTS

	# Find all of the neighbors of each ZIP code
	find_neighbors()

	# Create the districts
	create_districts(pop_per_district)

	print_dictionary(districts)

	print_district_pops()

	outline_districts()
	#print_dictionary(district_boundary)

	#output_individuals()
	output_outlines() 

	# Check to make sure sum of district populations equals the total population
	print("Population per district:", pop_per_district)
	print("Total population:", total_population)
