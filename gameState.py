import random
import Tkinter as tk

from hexagon import Hexagon, Point
from util import *

class GameState():	

	defaultBlocks = 15

	def __init__(self, rows, cols, nBlocks=None):
		if nBlocks is None:
			nBlocks = GameState.defaultBlocks
		if nBlocks > rows*cols:
			nBlocks = rows*cols-1
			print 'Warning: set nBlocks greater than rows*cols'

		self.rows = rows
		self.cols = cols

		self.grid = [[0]*cols for i in range(rows)]
		# 0 means empty
		# -1 means stone
		# 1 means pig

		self.pigTurn = False
		self.pigPosition = None
		
		# Add rocks
		t = nBlocks
		while True:
			if t == 0:
				break
			x = random.randrange(rows)
			y = random.randrange(cols)
			if self.grid[x][y] == 0:
				self.grid[x][y] = -1
				t -= 1

		# Add pig
		while True:
			buffer_row = rows//3
			buffer_col = cols//3
			x = random.randrange(buffer_row, rows-buffer_row)
			y = random.randrange(buffer_col, cols-buffer_col)
			if self.grid[x][y] == 0:
				self.pigPosition = (x, y)
				self.grid[x][y] = 1
				break

	def placeBlock(self, pos):
		x, y = pos
		self.grid[x][y] = -1

	def movePig(self, pos):
		x, y = pos
		if self.grid[x][y] != 0:
			print 'Error, trying to place pig in square that is not empty'
		i, j = self.pigPosition
		self.grid[i][j] = 0
		self.grid[x][y] = 1
		self.pigPosition = (x, y)

	def fieldIsEmpty(self, pos):
		x, y = pos
		return self.grid[x][y] == 0

	def fieldIsPig(self, pos):
		x, y = pos
		return self.grid[x][y] == 1

	def fieldIsStone(self, pos):
		x, y = pos
		return self.grid[x][y] == -1

	def isEscaped(self):
		i, j = self.pigPosition
		return i == 0 or i == self.cols-1 or j == 0 or j == self.rows-1

	def isCaptured(self):
		return optimalPigNextStep(self) is None

	def getLegalMoves(self, pos=None):
		if pos is None:
			pos = self.pigPosition
		
		x, y = pos
		
		#if it is a stone ignore
		if self.fieldIsStone(pos) == -1:
			return []

		edges = []

		#even row 
		if x%2 == 0:
			if x != 0:
				edges.append((x-1,y)) 
				# top right

			if x != self.rows-1:
				edges.append((x+1,y))
				# bottom right

			if y != self.cols-1:
				edges.append((x,y+1))
				# right

			if y != 0:
				edges.append((x, y-1))
				# left
				if x != 0:
					edges.append((x-1,y-1))
					# top left

				if x != self.rows - 1:
					edges.append((x+1, y-1))
					# bottom left

		#odd row
		else:
			edges.append((x-1,y))
			# top left

			if y != 0:
				edges.append((x, y-1))
				# left

				if x != self.rows-1:
					edges.append((x+1, y))
					# bottom left

			if y != self.cols -1:
				edges.append((x,y+1))
				# right

				edges.append((x-1, y+1))
				# top right

				if x != self.rows-1:
					edges.append((x+1, y+1))
					# bottom right

		# remove all edges *to* stones/blocked fields
		new_edges = []
		for v in edges:
			if self.fieldIsEmpty(v):
				new_edges.append(v)

		return new_edges
		
	def draw(self, window):
		prevCanvas = window.winfo_children()
		if prevCanvas:
			prevCanvas[0].destroy()

		canvas = tk.Canvas(window, width=500, height=500)
		canvas.configure(scrollregion=(0, 0, 400, 400))
		canvas.pack(side="top", fill="both", expand=True)
		offset = Hexagon.sideLength*1.1
		for row in range(self.rows):
			for col in range(self.cols):
				y = offset+row*Hexagon.sideLength*1.5
				if row%2 == 0:
					x = offset+col*Hexagon.sideLength*3**(0.5)
				else:
					x = offset+(col+0.5)*Hexagon.sideLength*3**(0.5)
				Hexagon(canvas, Point(x, y), self.grid[row][col])

