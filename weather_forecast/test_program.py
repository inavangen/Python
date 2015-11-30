# coding=utf-8
#!/usr/bin/python
# Test program
from forecast import *
import os
import time


class BaseCase():
	w = Weather()
	webpage = w.get_webpage("http://fil.nrk.no/yr/viktigestader/noreg.txt")
	xml_link_dict = w.get_xml_links(webpage, "Hannestad")

	xml_data_dict = w.check_buffer(xml_link_dict)

class TestCase1(BaseCase):


	def test_one(self):
                """4.1 Download the page for reference: http://www.islostarepeat.com/
                Check if your program creates the same document. """
 
                in_file = open("islostarepeat.txt", 'r').read()
                input1 = in_file[0:100]
               
                input2 = BaseCase.w.get_webpage("http://www.islostarepeat.com")
                input2 = input2[0:100]
               
                assert input1 == input2

	def test_two(self):
		"""4.2 Check if	Hannestad creates the link
		http://www.yr.no/place/Norway/stfold/Sarpsborg/Hannestad/forecast.xml
		"""
		s = "http://www.yr.no/place/Norway/Østfold/Sarpsborg/Hannestad/forecast.xml"
		ss = BaseCase.xml_link_dict["Ostfold-Sarpsborg-Hannestad"] 

		# Need to strip the url for uneccessary characters in order to work.
		s = s.replace(":", "")
		s = s.replace("/", "")
		s = s.replace(".", "")
		s = s.replace("Ø", "")
		ss = s.replace(":", "")
		ss = s.replace("/", "")
		ss = ss.replace(".", "")
		ss = ss.replace("Ø", "")
		assert ss == s

	def test_three(self):
		"""4.3 Ensure that temperature in Hannestad now is a valid numerical value
		between -50 and 50."""
		for key in BaseCase.xml_link_dict:
			weather_data_list  = BaseCase.w.get_weather_data(BaseCase.xml_data_dict[key], key)

		assert int(weather_data_list[1][0]) > -50 
		assert int(weather_data_list[1][0]) < 50


	def test_four(self):
		"""4.4 Create a dummy function that prints out a message before returning, much
		like the example in 4.4. Use the print out to conffirm that the bffeering
		works."""
		infile = "http://www.yr.no/place/Norway/stfold/Sarpsborg/Hannestad/forecast.xml"
		BaseCase.xml_link_dict["dummy"] = infile
		BaseCase.w.check_buffer(BaseCase.xml_link_dict)
		assert open("dummy.txt", "r")
		


	# TODO
	# Need to put time check in own func
	def test_five(self):
		"""4.4 Use the time stamp argument in 4.4 to test if the files expiration works
		through the following two tests. Create a dummy file with expired time
		stamp and ensure that it is replaced. And opposite, create a dummy file
		with unexpired time stamp and ensure that it isn't replaced."""

		old_file = open("old.txt", "w")
		old_file.write("1143728639")
		old_file.close()

		# Pass both files in the time check func and if both are true its oks
		assert BaseCase.w.check_time(open("old.txt", "r").read()) == 1

		new_file = open("new.txt", "w")
		t = str(int(time.time()))
		new_file.write(t)
		new_file.close()

		assert BaseCase.w.check_time(open("new.txt", "r").read()) == 0

		

	def test_six(self):
		"""	4.5 Ensure (again) that the temperature in Hannestad at (next) 13:00 is valid
		between -50 and 50"""


		for key in BaseCase.xml_data_dict:
			xml_data = BaseCase.xml_data_dict[key]
			weather_data = BaseCase.w.get_weather_data(xml_data, key)
			#all_weather_data.append(weather_data)
			temp_list = BaseCase.w.print_forecast(weather_data, 13, 00)

		i = 0
		for val in temp_list:	
			assert int(temp_list[i]) > -50 
			assert int(temp_list[i]) < 50
			i += 1
