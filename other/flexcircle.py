#!/usr/bin/python
# Oppgave 3.3. Flext circle calculations
import math
import sys

class FlexCircle(object):
	
	def __init__(self, radius):
		self._radius = radius
		self._area = (radius*radius*math.pi)
		self._perimeter = (2*math.pi*radius)


	def set_radius(self, d):
		"""Sets radius of circle."""
		self.is_number(d)
		self._radius = d
		self._area = (d*d*math.pi)
		self._perimeter = (2*math.pi*d)

	def get_radius(self):
		"""Gets radius of circle."""
		return self._radius

	radius = property(fget=get_radius, fset=set_radius)

	# Area funcitons
	def set_area(self, d):
		"""Sets area of circle."""
		self.is_number(d)
		self._area = d
		self._radius = math.sqrt(d/math.pi)
		self._perimeter = self._radius*2*math.pi

	def get_area(self):
		"""Gets area of circle."""
		return self._area

	area = property(fget=get_area, fset=set_area)

	# Perimeter funcitons
	def set_perimeter(self, d):
		"""Sets perimeter of circle."""
		self.is_number(d)
		self._perimeter = d
		self._radius = (d/math.pi)/2
		self._area = (self._radius*self._radius*math.pi)

	def get_perimeter(self):
		"""Gets perimeter of circle."""
		return self._perimeter

	perimeter = property(fget=get_perimeter, fset=set_perimeter)

	def is_number(self, d):
		"""Checks if the agument is a digit. Prints error and 
		exits script if argument is not a number """

		try:
			float(d)
			return 0
		except ValueError:
			print "Error! Please enter only numbers. Exiting script."
			sys.exit()
				

# Testing
if __name__ == '__main__':
	c = FlexCircle(radius = 2)
	print c.area
	c.perimeter = 1.5
	print c.radius
	c.area = 0.6
	print c.perimeter

	
	#print c.radius
	#print "----------------------------"
	#print "Area: {} | Radius: {} | Perimeter: {} ".format(c.area, c.radius, c.perimeter)
	#print "----------------------------"
	#c.perimeter = 31.4
	#print c.perimeter
	#print "----------------------------"
	#print "Area: {} | Radius: {} | Perimeter: {} ".format(c.area, c.radius, c.perimeter)
	#print "----------------------------"
	#c.area = 123
	#print c.area
	#print math.sqrt(100)/math.pi
	#print "----------------------------"
	#print "Area: {} | Radius: {} | Perimeter: {} ".format(c.area, c.radius, c.perimeter)
	#print "----------------------------"
	
	