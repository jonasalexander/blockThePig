import random
import Tkinter as tk

from hexagon import Hexagon, Point

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

		self.isCaptured = False
		self.pigPosition = None
		
		# Add rocks
		t = nBlocks
		while True:
			x = random.randrange(rows)
			y = random.randrange(cols)
			if self.grid[x][y] == 0:
				self.grid[x][y] = -1
				t -= 1
			if t == 0:
				break

		# Add pig
		while True:
			x = random.randrange(rows)
			y = random.randrange(cols)
			if self.grid[x][y] == 0:
				self.pigPosition = (x, y)
				self.grid[x][y] = 1
				break

	def placeBlock(self, x, y):
		return
		# self.grid[x][y]

	def movePig(self, x, y):
		if self.grid[x][y] != 0:
			print 'Error, trying to place pig in square that is not empty'
		i, j = self.pigPosition
		self.grid[i][j] = 0
		self.grid[x][y] = 1
		self.pigPosition = (x, y)

	def isEscaped(self):
		i, j = self.pigPosition
		return i == 0 or i == self.cols-1 or j == 0 or j == self.rows-1

	def isCaptured(self):
		return True

	def getLegalMoves(self):
		return None
		
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

