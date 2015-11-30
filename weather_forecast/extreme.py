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
					try:
						xml_data = urllib.urlopen(xml_link_dict[key]).read()
					except:
						print "Failed to retrieve XML-data (Please check your internet connection."
						exit(0)

					buffer_file = open(key+".txt", "w")
					buffer_file.write(xml_data)
					buffer_file.write(new_time)
				else:
					temp_file = open(key+".txt", "r").read()
					xml_data = temp_file

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
			xml_link_dict[new_file_name] = entry

		return xml_link_dict

	def get_webpage(self, url):
		""" Returns the textfile that is found on the url"""
		try:
			return urllib.urlopen(url).read()
		except:
			return 0

	def extreme_weather(self, all_weather_data):
		"""To avoid overriding yr.no's bandwidth, the code is limited
		to the first 100 entries in noreg.txt. all_weather_data contains
		all collected data of weather. Including names"""

		hottest_name = ""
		hottest_temp = -1000
		coldest_name = ""
		coldest_temp = 1000

		for weather_list in all_weather_data:
			temp_list = weather_list[1]
			#print str(weather_list[2])
			place = weather_list[8]
			#print weather_list[9]

			i = 0
			for value in temp_list:
				if(int(temp_list[i]) > hottest_temp):
					hottest_temp = int(temp_list[i])
					hottest_name = place
				elif(int(temp_list[i]) < coldest_temp):
					coldest_temp = int(temp_list[i])
					coldest_name = place
				i += 1

		print "Hottest: {}, {}, \tColdest: {}, {}".format(hottest_name, hottest_temp, coldest_name, coldest_temp)
		return 0
	
	def create_forecast(self, place, hour, minute):
		"""Takes place, hour, minutes as aguments and prints weather forecast"""
		
		url = "http://fil.nrk.no/yr/viktigestader/noreg.txt"
		webpage = self.get_webpage(url)
		print "Running extreme script..."

		xml_link_dict = self.get_xml_links(webpage, place)
		xml_data_dict = self.check_buffer(xml_link_dict)

		all_weather_data = []
		for key in xml_data_dict:
			xml_data = xml_data_dict[key]
			weather_data = self.get_weather_data(xml_data, key)
			all_weather_data.append(weather_data)
			#temp_list = self.print_forecast(weather_data, hour, minute)

		dump = self.extreme_weather(all_weather_data)

if __name__ == '__main__':
	w = Weather()
	w.create_forecast("", 13, 00)
	