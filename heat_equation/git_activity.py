# coding=utf-8
#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import argparse
from random import randint as r
plt.rcParams.update({'font.size': 7})

def get_log(path):
	"""Takes a path to a git repository as a parameter and retuns 
	a string containing a git log."""
	# Could possibly use Popen instead of os.
	try:
		os.chdir(path)
		log = os.popen('git log').read()
		return log
	except:
		print "ERROR! Could not open git log. Requires a path as an argument. Make sure your path is a git repository."
		exit(1)

def get_date(log):
	""" Takes a git log as a string as parameter and uses regex to
	return a list of all days in the formal: dd mm yyyy """
	pattern_month = re.compile(r"Date:\s+\w+\s(?P<month>\w+)")
	pattern_day = re.compile(r"Date:\s+\w+\s\w+\s(?P<date>\d+)")
	pattern_year = re.compile(r"Date:\s+\w+\s\w+\s\d+\s\d+:\d+:\d+\s(?P<year>\d+)\s")

	day_list = re.findall(pattern_day, log)
	month_list = re.findall(pattern_month, log)
	year_list = re.findall(pattern_year, log)

	new_date_list = day_list
	for i in range(len(day_list)):
		new_date_list[i] = ("{} {} {}".format(day_list[i], month_list[i], year_list[i])) 

	return new_date_list	

def get_author(log):
	""" Takes a git log as a string as parameter and uses regex to
	return a list of all authors. """
	pattern_author = re.compile(r"Author:\s(?P<author>\w+)\s")
	author_list = re.findall(pattern_author, log)
	return author_list

def organize_data(author_list, date_list):
	"""Takes a list of authors and a list of dates as a parameter.
	Returns a dictionary containg organized data used for plotting."""
	# Data structure is a dictionary using dates as keys
	# and another dict as value. This dict contains authors
	# as key and value is the number of commits for that author
	# for that day.
	datedict = {}
	for i in range(len(date_list)):
		if (date_list[i] in datedict.keys()):
			author_temp_dict = datedict[date_list[i]]
			if (author_list[i] in author_temp_dict.keys()):
				author_temp_dict[author_list[i]] += 1
			else:
				author_temp_dict[author_list[i]] = 1

			datedict[date_list[i]] = author_temp_dict 

		else:
			authordict = {}
			datedict[date_list[i]] = authordict
			author_temp_dict = datedict[date_list[i]]
			author_temp_dict[author_list[i]] = 1
			datedict[date_list[i]] = author_temp_dict 

	return datedict


def plot_stuff(datedict, date_list, author_list, out):
	"""Uses data(datedict, date_list, author_list) from git log 
	to plot a nice histogram. If out is true, an image is saved
	of the plot."""
	
	data_list = []
	# One array per commiter, that represent one day. Will be 0 
	# if 0 commits on that spesific day, 1 if 1 commit an so on	
	X = np.arange(len(datedict))

	author_dict ={}
	# Author list should be of length of the number of days(datdict)
	for author in author_list:
		x = np.zeros(len(datedict))
		author_dict[author] = x

	# Enumerates every value in datedict
	for i, values in enumerate(datedict.values()):
		for key, value in values.items():
			author_dict[key][i] = value

	# To select random color. Number of colors = number of unique authors
	color_list = {}
	for author in author_dict:
		col = '#%02x%02x%02x' % (r(0,0xFF),r(0,0xFF),r(0,0xFF))
		color_list[author] = col
	
	# last_author used for stacking bars on top of each other
	last_author = np.zeros(len(X)) 	
	# Creates a bar for each author's X-list(containing number of commits)
	for i in author_dict:
		plt.bar(X, author_dict[i], bottom=last_author, width = 0.5, color=color_list[i])
		last_author = author_dict[i]

	plt.xticks(X, datedict.keys(), rotation=50)
	plt.legend(author_dict) 
	# If output file is choosen, save plot.
	if out:
		plt.savefig(out)
		print "Plot saved as {}.".format(out)
	
	plt.show()

def main():
	"""Calls necessary functions to create a nice plot of 
	git activity. """
	parser = argparse.ArgumentParser(description='Git activity')
	parser.add_argument('path', nargs='?', type = str, help="Path to git-directory") #TODO
	parser.add_argument('-out', nargs='?', help="Save plot as user-specified file") 
	args = parser.parse_args() 

	log = get_log(args.path)
	date_list = get_date(log)
	author_list = get_author(log)
	datedict = organize_data(author_list, date_list)
	something = plot_stuff(datedict, date_list, author_list, args.out)

if __name__ == '__main__':
	main()

	