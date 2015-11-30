# coding=utf-8
#!/usr/bin/python
import urllib
import re
import datetime
import time
import os

class Weather:

	def get_weather_data(self, xml_data, key):
		"""Returns a list of lists with weather data based on the
		given xml_data (one file, not dict) and key (navn)"""
		
		weatherdata = []
		# Long regex that pics out all the necessary data in on call.
		all_data_pattern = re.compile(r"<time\sfrom=\"(?P<fromDate>\d+-\d+-\d+)T(?P<fromtime>\d+:\d+:\d+)\"\sto=\"(?P<toDate>\d+-\d+-\d+)T(?P<totime>\d+:\d+:\d+)\".*\n.*\n.*name=\"(?P<symbol>.*)\"\sv.*\n.*\svalue=\"(?P<prec>\d+\.?\d?).*\n.*\n.*\n.*mps=\"(?P<wind>\d+.\d).*\n.*\svalue=\"(?P<temp>\d+)\".*", re.U|re.M|re.I)
		weather_data = re.findall(all_data_pattern, xml_data)
		# Defines a munch of list
		fromDate_list, fromHour_list, toDate_list, toHour_list, \
		symbol_list, prec_list, wind_list, temp_list \
		= ([] for x in range(8)) 
		
		i = 0
		for entry in weather_data:
			fromDate_list.append(weather_data[i][0])
			fromHour_list.append(weather_data[i][1])			
			toDate_list.append(weather_data[i][2])
			toHour_list.append(weather_data[i][3])
			symbol_list.append(weather_data[i][4])
			prec_list.append(weather_data[i][5])
			wind_list.append(weather_data[i][6])
			temp_list.append(weather_data[i][7])
			i +=1
		# Creates a list of lists of weather data and returns it
		weather_data_list = [symbol_list, temp_list, wind_list, prec_list, fromDate_list, toDate_list, fromHour_list, toHour_list, key]
		return weather_data_list

	def print_forecast(self, weather_data_list, hour, minute):
		""" Takes a weather datalist as a parameter which contains
		all the weather data retrieved from a xml-file, as well as 
		hour and minute which will be used to find the correct weather
		forecast for the time selected. """

		symbol_list, temp_list, wind_list, prec_list, fromDate_list, \
		toDate_list, fromHour_list, toHour_list, place \
		= (weather_data_list[x] for x in range(9)) 

		pattern = "%Y-%m-%d %H:%M:%S"

		# Current time converted to epoch (for easier comparasion)
		current_date_time = time.strftime(pattern)
		current_epoch = int(time.mktime(time.strptime(current_date_time, pattern)))

		# Selected time (from input) converted to epoch
		selected_date = time.strftime("%Y-%m-%d")
		selected_date_time = ("{} {}:{}:00").format(selected_date, hour, minute)
		selected_epoch = int(time.mktime(time.strptime(selected_date_time, pattern)))

		# if the selected time havent yet been (is in the future)
		if(selected_epoch > current_epoch):
			print "Finding forecast for current day...\n"
			
			d = datetime.datetime.now()
			current_date =("{}-{:0>2}-{:0>2}").format(d.year, d.month, d.day)

			i = 0
			for entry in fromHour_list: 
				# Converts from- and to-time to epoch
				from_data = str("{} {}").format(current_date, fromHour_list[i]) 
				to_data = str("{} {}").format(current_date, toHour_list[i]) 
				epoch_from = int(time.mktime(time.strptime(from_data, pattern)))
				epoch_to = int(time.mktime(time.strptime(to_data, pattern)))
				
				#Check if current date matches date and that time is found between epoch from and to
				if ((current_date == fromDate_list[i]) and (selected_epoch >= epoch_from)):
					print "{} {} to {} {}".format(fromDate_list[i], fromHour_list[i], toDate_list[i], toHour_list[i])
					print "{}: {}, rain:{}mm, wind:{}mps, temp:{}deg ".format(place, str(symbol_list[i]), str(prec_list[i]), str(wind_list[i]), str(temp_list[i]))
					print "-----------------------------\n"

				i += 1

		# Selected time has already been, find for next day
		else:
			print "Finding forecast for next day...\n"
			# Gets date and time exactly one day in the future.
			d_now = datetime.datetime.now()
			d = d_now.replace(hour = int(hour), minute = int(minute))
			d += datetime.timedelta(days=1)

			# Get all the necesary data
			next_date = ("{}-{:0>2}-{:0>2}").format(d.year, d.month, d.day)
			# Get the right format
			next_date_format = ("{}-{:0>2}-{:0>2} {:0>2}:{:0>2}:00").format(d.year, d.month, d.day, d.hour, d.minute)
			# Convert to epoch
			next_date_epoch = int(time.mktime(time.strptime(next_date_format, pattern)))

			i = 0
			for entry in toHour_list:
				# for each iteration, calculate new epoch
				from_data = str("{} {}").format(next_date, fromHour_list[i]) 
				to_data = str("{} {}").format(next_date, toHour_list[i]) 
				epoch_from = int(time.mktime(time.strptime(from_data, pattern)))
				epoch_to = int(time.mktime(time.strptime(to_data, pattern)))

				# Need to get new selected epoch for next day
				if ((next_date == fromDate_list[i]) and (next_date_epoch >= epoch_from) and (next_date_epoch <= epoch_to)):
					print "\n-----------------------------"
					print "{} {} to {} {}".format(fromDate_list[i], fromHour_list[i], toDate_list[i], toHour_list[i])
					print "{}: {}, rain:{}mm, wind:{}mps, temp:{}deg c".format(place, str(symbol_list[i]), str(prec_list[i]), str(wind_list[i]), str(temp_list[i]))
					print "-----------------------------"
				i += 1
				
		# Used for testing
		return temp_list

	def check_time(self, buffer_file):
		"""Takes a buffer file as parameter and checks if
		more than 6 hours has passed (using epoch time).
		If more than 6 hours, it will retrieve a new file, 
		otherwise, return the old one. """
		
		# Used for testing
		if(isinstance(buffer_file, str)):
			old_time = float(buffer_file)

		else:
			lines = buffer_file.readlines()
			old_time = float(lines[len(buffer_file.readlines())-1])
		new_time = float(time.time()) #Current timestamp
		diff = float(new_time - old_time)

		if (diff > 21600):
			return 1
		else:
			return 0

	def check_buffer(self, xml_link_dict):
		""" Checks dir for corresponding files. If they dont exsist
		simply create them. If file already exsist, check if 6 hours
		has passed and if so, retrieve new xml data """

		print "Checking buffer (this might take a while)..."
		xml_data_dict = {}

		for key in xml_link_dict:
			
			# File exsist. Simple read
			try:
				buffer_file = open(key+".txt", "r")
				
				okay = self.check_time(buffer_file)

				# 21600 is epoch time for 6 hours
				if (okay == 1):
					print "More than 6 hours has passed."
					try:
						xml_data = urllib.urlopen(xml_link_dict[key]).read()
					except:
						print "Failed to retrieve XML-data (Please check your internet connection."
						exit(0)

					buffer_file = open(key+".txt", "w")
					buffer_file.write(xml_data)
					buffer_file.write(new_time)
				else:
					print "Less than 6 hours has passed."
					temp_file = open(key+".txt", "r").read()
					xml_data = temp_file
					print "Found old file."

				buffer_file.close()
				xml_data_dict[key] = xml_data


			# Need to retrieve new file
			except:
				try:
					xml_data = urllib.urlopen(xml_link_dict[key]).read() # Retrieves xml data from online
				except:
					print "Failed to retrieve XML-data (Please check your internet connection."
					exit(0)
				# Remove unnecessary data from xml_data
	 			temp_pattern = re.compile(r"<tabular>.*<\/tabular>", re.DOTALL)
	 			temp_xml = re.findall(temp_pattern, xml_data)
	 			if temp_xml:
	 				xml_data = str(temp_xml[0])

				buffer_file = open(key+".txt", "w") # Opens new file
				buffer_file.write(xml_data) # Writes xml_data to file
				buffer_file.write("\n" + str(time.time())) # Writes timestamp	
				buffer_file.close()
 				print "Created new file."	

				# Add data to new dict
				xml_data_dict[key] = xml_data
				# A new dict with retrieved xml data (opened text, not links)
		return xml_data_dict

	
	def get_xml_links(self, webpage, place):
		"""Returns a dictionary with the xml_pages of the 
		selected locations."""
		xml_link_dict = {} #defines a dictionary
		xml_list = [] #holds result from re-calls. is to be put in xml_link_dict

		if (place == ""):
			empty_pattern = re.compile(r"\t\w+\t\d.*\t.*\t.*\t\d+\..*\t(?P<XML>.*)", re.U|re.M|re.I)			
			xml_list = re.findall(empty_pattern, webpage)	

		else:
			# First look for matching stadnamn
			stadnamn_pattern = re.compile(r"\t.*" + re.escape(place) + ".*\t\d.*\t.*\t.*\t\d+\..*\t(?P<XML>.*)", re.U|re.M|re.I)
			xml_list = re.findall(stadnamn_pattern, webpage)	
			# If no matches found on stadnamn, try kommune
			if (len(xml_list) == 0):
				kommune_pattern = re.compile(r"\t.*" + re.escape(place) + ".*\t.*\t\d+\..*\t(?P<XML>.*)", re.U|re.M|re.I)
				xml_list = re.findall(kommune_pattern, webpage)
				# If no matches found on kommune, try fylke
				if (len(xml_list) == 0):
					fylke_pattern = re.compile(r"\t.*" + re.escape(place) + ".*\t\d+\..*\t(?P<XML>.*)", re.U|re.M|re.I)
					xml_list = re.findall(fylke_pattern, webpage)
					# If no matches at all
					if (len(xml_list) == 0):
						print "No matches found on either stadnamn, kommune or fylke."

		xml_list = xml_list[0:100] 

		# Add all xml_list entries xml_link_dict
		for entry in xml_list:

			#Find a suiting filename
			file_name = re.findall(r"/Norway/(?P<name>.*)/forecast", entry)

			#Some modifications to file_name
			new_file_name = str(file_name[0].replace("/", "-"))
			new_file_name = new_file_name.replace("Ø", "O")
			new_file_name = new_file_name.replace("Æ", "AE")
			new_file_name = new_file_name.replace("Å", "A")

			xml_link_dict[new_file_name] = entry

		return xml_link_dict

	def get_webpage(self, url):
		""" Returns the textfile that is found on the url"""
		try:
			return urllib.urlopen(url).read()
		except:
			return 0
	
	def create_forecast(self, place, hour, minute):
		"""Takes place, hour, minutes as aguments and prints 
		weather forecast"""
	
		url = "http://fil.nrk.no/yr/viktigestader/noreg.txt"
		# Retrieves the noreg.txt
		
		webpage = self.get_webpage(url)
		if (webpage == 0):
			print "Failed to retrieve webpage (Please check your internet connection)."
			exit(0)

		# dict of LINK (unopened) to all xml files
		xml_link_dict = self.get_xml_links(webpage, place)

		xml_data_dict = self.check_buffer(xml_link_dict)

		all_weather_data = []

		for key in xml_data_dict:
			xml_data = xml_data_dict[key]
			weather_data = self.get_weather_data(xml_data, key)
			all_weather_data.append(weather_data)
			temp_list = self.print_forecast(weather_data, hour, minute)

if __name__ == '__main__':
	w = Weather()

	place = raw_input('Type location: ')
	hour = "n"
	minute = "n"
	while(hour >= 24 or hour < 0 or isinstance(hour, int) == False):
		try:
			hour = int(raw_input('Type hour(0-23): '))
		except:
			print "Only accepts numbers 0-23"
		
	while(minute >= 60 or minute < 0 or isinstance(minute, int)== False):
		try: 
			minute = int(raw_input('Type minute(0-59): '))
		except:
			print "Only accepts numbers 0-59"
	# If input is * convert it to empty string
	place = re.sub("[*]","", place)
	w.create_forecast(place, hour, minute)
	
