#!/usr/bin/python
# Oppgave 3.2. Define a class named Circle which is constructed just by a radiu
import math

class Circle(object):
	
	def __init__(self, radius):
		self.radius = radius

	def area(self):
		"""Returns computed area of the circle."""
		#print (self.radius*self.radius*math.pi)
		circle_area = (self.radius*self.radius*math.pi)
		return circle_area

	def perimeter(self):
		"""returns computed perimeter."""		
		#print (2*math.pi*self.radius)
		area_perimeter = (2*math.pi*self.radius)
		return area_perimeter

# Main method -ish
if __name__ == '__main__':
	c = Circle(radius = 10)
	print "Area = {0}, Perimeter: {1}".format(c.area(), c.perimeter())
	