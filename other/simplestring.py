#!/usr/bin/python
# Oppgave 3.1 String class

# Trengs det noe docstring her

class SimpleString:
	
	def getString(self):
		"""Returns a string from console input."""
		#print "get string called"
		self.input_data = raw_input('Input: ')
	
	def printString(self):
		"""Prints the string in upper case."""		
		#print "print string in upper case"
		print self.input_data.upper()


if __name__ == '__main__':
	s = SimpleString()
	s.getString()
	s.printString()