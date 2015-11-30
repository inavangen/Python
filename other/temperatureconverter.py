#!/usr/bin/python
# Oppgave 2.2
import sys

fahrenheit = float(sys.argv[1])
celcius = (fahrenheit-32)/1.8
print ("%.1f Fahrenheit is equal to %.1f Celsius.") % (fahrenheit, celcius)
