#!/usr/bin/python
# Oppgave 2.4
import sys

for element in sys.argv[1:]:

	wordCount = 0
	inFile = open(element, 'r')
	lines = inFile.readlines()
	for line in lines:
		words = line.split("")
		wordCount += len(words)
		
	print ("%s: %d") % (element, wordCount)

inFile.close()
