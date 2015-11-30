#!/usr/bin/python
# Oppgave 2.3
import sys

for element in sys.argv[1:]:

	linesCount = 0

	inFile = open(element, 'r')
	for line in inFile:
		linesCount += 1

	print ("%s: %d") % (element, linesCount)

inFile.close()