#!/usr/bin/python
# Oppgave 3.4 Specialized ranking function
import sys

if __name__ == '__main__':

	mydictionary = {}
	input_file = open('data.log', 'r')

	lines = input_file.readlines()
	for line in lines:
		if "CPU" in line:
			words = line.split()

			# If name already exsist, only append new cpu value
			if words[1] in mydictionary.keys():
				mydictionary[words[1]].append(words[3])
			# Else create a new cpu list with the cpu value
			else:
				cpu_list = [words[3]]
				mydictionary[words[1]] = cpu_list


	for keys, value in mydictionary.iteritems():
		value.sort()
		print "Test name: {}".format(keys)
		print "CPU time:  %.1f s (min)" % float(min(value))
		avg_sum = 0
		for s in value:
			avg_sum += float(s)

		print "\t   %.1f s (avg)" % float(avg_sum/len(value))
		print "\t   %.1f s (max)\n" % float(max(value))

	
	input_file.close()
