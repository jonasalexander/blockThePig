import tkinter as tk

from util import *

class Point():

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return 'x: ' + str(self.x) + '; y: ' + str(self.y)

class Hexagon():
	sideLength = 20

	def __init__(self, canvas, center, stateInt):
		# Draw isosceles hexagon
		self.canvas = canvas
		self.centerX = center.x
		self.centerY = center.y
		self.state = STATES[stateInt]

		if self.state == 'pig':
			fill = 'red'
		elif self.state == 'block':
			fill = 'black'
		elif self.state == 'free':
			fill = 'white'
		else:
			print ('Error, unrecognized state in Hexagons init func')

		a = Hexagon.sideLength*3**(0.5)/2 # by pythoagoras
		p1 = Point(center.x-a, center.y-Hexagon.sideLength/2)
		p2 = Point(center.x-a, center.y+Hexagon.sideLength/2)
		p3 = Point(center.x, center.y+Hexagon.sideLength)
		p4 = Point(center.x+a, center.y+Hexagon.sideLength/2)
		p5 = Point(center.x+a, center.y-Hexagon.sideLength/2)
		p6 = Point(center.x, center.y-Hexagon.sideLength)

		canvas.create_polygon([	p1.x,p1.y,
								p2.x,p2.y,
								p3.x,p3.y,
								p4.x,p4.y,
								p5.x,p5.y,
								p6.x,p6.y], 
			outline='black', fill=fill, width=2)

		return

