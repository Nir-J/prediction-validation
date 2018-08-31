import sys

def parse_line(line):
	"""
	Parses lines in input files
	param:
		lines : (string) Input line
	ret:
		hour : (int) 
		name : (string) Stock name
		value : (int) Value of stock at that hour
	"""
	hour, name, value = line.strip().split("|")
	return int(hour), name, float(value)

def sum_and_elements(hour, stocks_dict):
	"""
	Returns total of stock values and number of stocks in specified hour
	Params:
		hour : (int) 
		stocks_dict : (dict) Dictionary containing all stocks
	ret
		(total, count) : (int, int) Sum of stock values, number of stocks
	"""
	total = 0
	count = 0
	for key, value in stocks_dict[hour].items():
		# If stock was present in both files.
		if value[1]:
			# value[0] is the error in prediction value for that stock.
			total += value[0]
			count += 1
	return (total, count)

def parse_input_files(actual_file, predicted_file, window_file):
	"""
	Reads values from all the input files.
	Params:
		actual_file : (string) path to actual file.
		predicted_file: (string) path to predicted file.
		window_file: (string) path to window file.
	ret:
		stocks_dict : {hour:{'stock_name':(value, Bool)}}
		window: (int)
		maxhour: (int) Maximum hour in actual file.
	"""


	# Stores stock values on hourly basis, where each hour has a dictionary.
	# entry. Ex: stocks_dict[1] = {'name1':(value1, False), 'name2':(value2, False)}
	# The second entry is to keep track whether stock was present in the actual
	# file

	stocks_dict = {}
	# Maximum hour and Minimum hour in our input
	maxhour = None
	minhour = None

	# Read predicted values first as we need all of them
	with open(predicted_file, "r") as f:
		# Assuming everything will fit in memory, as it was mentioned.
		lines = f.readlines()
		for line in lines:
			hour, name, value = parse_line(line)
			if hour not in stocks_dict:
				stocks_dict[hour] = {}

			# Add tuple (value, False). False because we do not know whether it
			# is present in the actulaL file yet.
			stocks_dict[hour][name] = (value, False)

	# Read only relevant actual values
	with open(actual_file, "r") as f:
		# Read line by line, we only need to store some of it.
		line = f.readline()
		while line:
			hour, name, value = parse_line(line)
			# Consider only if hour, stock was present in the predicted file
			if hour in stocks_dict:
				if name in stocks_dict[hour]:
					# Calculate and store the difference. (Error in prediction)
					# Also make the entry True as it is present in both files.
					stocks_dict[hour][name] = (abs(stocks_dict[hour][name][0] - value), True)
			
			maxhour = hour;
			if not minhour:
				minhour = hour
			line = f.readline()

	# Read window file
	window = None
	with open(window_file, "r") as f:
		window = int(f.read())

	return (stocks_dict, window, minhour, maxhour)


def main():

	if len(sys.argv) != 5:
		print "Arguments: [actual_file] [predicted_file] [window_file] [output_path]"
		exit(1)

	# Store paths
	actual_file = sys.argv[1]
	predicted_file = sys.argv[2]
	window_file = sys.argv[3]
	output_file = sys.argv[4]


	stocks_dict, window, minhour, maxhour = \
				parse_input_files(actual_file, predicted_file, window_file)

	# At this point:
	# 
	# stocks_dict: Has 'Error in prediction values' for
	# each stock at a particular hour
	# Ex: stocks_dict[1]: {'name1': (error, True), 'name2': (error, True)}
	#
	# minhour : Minimum hour to start sliding window from
	# maxhour : Maximum hour to consider while calculating average


	# Calculate total error and number of stocks in each hour
	# Hours start from 1, so adding default -1, 0 for hour 0
	sums = [-1]
	counts = [0]
	# Hour starts from 1
	for hour in range(1, maxhour+1):
		# We might not have any predicted stock for the given hour
		if hour in stocks_dict:
			total, count = sum_and_elements(hour, stocks_dict)
			sums.append(total)
			counts.append(count)
		else:
			# Zero stocks for that hour
			sums.append(-1)
			counts.append(0)

	# At this point we do not need the dictionary anymore
	del(stocks_dict)

	# Using sliding window approach for calculating average error value
	# in a particular window

	# current_elements: Number of stocks included in current window.
	# current_sum: Sum of errors of each hour in current window
	current_elements = 0
	current_sum = 0

	with open(output_file, "w") as f:
		
		# Separate for the first window
		for i in range(minhour, minhour+window):
			# Only consider valid hours
			if sums[i] != -1:
				current_sum += sums[i]
				current_elements += counts[i]
		
		if current_elements != 0:
			line = "{}|{}|{:.2f}\n".format(minhour, minhour+window-1, current_sum/current_elements)
		else:
			line = "{}|{}|NA\n".format(minhour, minhour+window-1)
		f.write(line)

		for start in range(minhour+1, maxhour-window+2):
			
			end = start + window -1

			# Subtract errors of hour which was just removed from the window
			# (If valid)
			if sums[start-1] != -1:
				current_sum -= sums[start-1]
				current_elements -= counts[start-1]

			# Add errors of hour which was just added to the window, (If valid)
			if sums[end] != -1:
				current_sum += sums[end]
				current_elements += counts[end]

			if current_elements != 0:
				line = "{}|{}|{:.2f}\n".format(start, end, current_sum/current_elements)
			else:
				line = "{}|{}|NA\n".format(start, end)
			f.write(line)

if __name__ == "__main__":
	main()