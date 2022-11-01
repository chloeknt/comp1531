import math

class Circle:
	def __init__(self, radius):
		self.radius = radius

	def circumference(self):
		return (self.radius * 2) * 3.14

	def area(self):
		return pow(self.radius, 2) * 3.14
