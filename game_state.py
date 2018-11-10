import random

class GameState():	

	defaultBlocks = 15

	def __init__(self, rows, cols, nBlocks=None):
		if nBlocks is None:
			nBlocks = GameState.defaultBlocks
		if nBlocks > rows*cols:
			nBlocks = rows*cols-1
			print 'Warning: set nBlocks greater than rows*cols'

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
		self.grid[x][y]

	def movePig(self, x, y):
		return

	def isCaptured(self):
		return True

	def getLegalMoves(self):
		return None

