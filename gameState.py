import random
import Tkinter as tk

from hexagon import Hexagon, Point
from util import *
from stoneAgent import stoneAgent
from pigAgent import pigAgent

class GameState():	

	defaultBlocks = 15

	def __init__(self, rows, cols, players, numBlocks=None, numPigs=None, quiet=False):
		if numBlocks is None:
			numBlocks = GameState.defaultBlocks
		if numBlocks > rows*cols:
			numBlocks = rows*cols-1
			print ('Warning: set numBlocks greater than rows*cols')

		if numPigs is None:
			numPigs = 1

		self.quiet = quiet
		self.rows = rows
		self.cols = cols
		self.numPigs = numPigs

		self.grid = [[0]*cols for i in range(rows)]
		# 0 means empty
		# -1 means stone
		# 1 means pig

		self.pigPositions = []

		self.turn = 0 # index into self.players
		self.players = players

		# last move (to be able to deduce optimal move from optimal game state)
		self.lastMove = None
		


		# Add pig(s)
		t = numPigs

 		while True:
			if t == 0:
				break
			buffer_row = rows//3
			buffer_col = cols//3
			x = random.randrange(buffer_row, rows - buffer_row)
			y = random.randrange(buffer_col, cols - buffer_col)
			if self.grid[x][y] == 0:
				self.pigPositions.append((x, y))
				self.grid[x][y] = 1
				t -= 1

		# Add rocks
		t = numBlocks
		while True:
			if t == 0:
				break
			x = random.randrange(rows)
			y = random.randrange(cols)
			if self.grid[x][y] == 0:
				self.grid[x][y] = -1
				t -= 1

		# self.grid[0][0]  = -1
		# self.grid[0][1]  = -1
		# self.grid[0][2]  = -1
		# self.grid[0][3]  = -1
		# self.grid[0][4]  = -1
		# self.grid[0][5]  = -1
		# self.grid[5][0]  = -1
		# self.grid[5][1]  = -1
		# self.grid[5][2]  = -1
		# self.grid[5][3]  = -1
		# self.grid[5][4]  = -1
		# self.grid[5][5]  = -1
		# self.grid[0][0]  = -1
		# self.grid[1][0]  = -1
		# self.grid[2][0]  = -1
		# self.grid[3][0]  = -1
		# self.grid[4][0]  = -1
		# self.grid[5][0]  = -1
		# self.grid[0][5]  = -1
		# self.grid[1][5]  = -1
		# self.grid[2][5]  = -1
		# self.grid[3][5]  = -1
		# self.grid[5][0]  = -1
		





		

	def incrementTurn(self):
		self.turn = (self.turn+1)%len(self.players)


	def placeBlock(self, pos):
		x, y = pos
		self.grid[x][y] = -1

		self.incrementTurn()
		self.lastMove = pos

	def movePig(self, pos, pigId):
		x, y = pos
		if self.grid[x][y] != 0:
			print ('Error, trying to place pig in square that is not empty')
		i, j = self.pigPositions[pigId]
		self.grid[i][j] = 0
		self.grid[x][y] = 1
		self.pigPositions[pigId] = (x, y)

		self.incrementTurn()
		self.lastMove = pos

	def isPigTurn(self):
		return self.players[self.turn].isPig

	def distanceToNearestPig(self, pos):
		shortestPathLen = float("inf")
		path = None
		for pigId in range(self.numPigs):
			path = BFSPath(self, pigId, pos)
			if path is None:
				continue
			elif shortestPathLen > len(path):
				shortestPathLen = len(path)
		return shortestPathLen

	def fieldIsAlmostEmpty(self, pos):
		x,y = pos
		return (self.grid[x][y] != -1)
	
	
	def fieldIsEmpty(self, pos):
		x, y = pos
		return self.grid[x][y] == 0

	def fieldIsPig(self, pos):
		x, y = pos
		return self.grid[x][y] == 1

	def fieldIsStone(self, pos):
		x, y = pos
		return self.grid[x][y] == -1

	def isEscaped(self, pigId):
		i, j = self.pigPositions[pigId]
		#print "i, j", i, j
		return (i == 0 or i == self.cols-1 or j == 0 or j == self.rows-1)
			#print "pig escaped:", pigId
		# 	self.players[pigId].isEscaped = True
		# 	return True
		# else:
		# 	return False

		# if i == 0 or i == self.cols-1 or j == 0 or j == self.rows-1:
		# 	for ind, x in enumerate(self.players):
		# 		if x.isPig:
		# 			if x.pigId == pigId:
		# 				bad_pig = self.players.pop(ind)
		# 				print('b', bad_pig)
		# 	return True
		# return False
		# if(i == 0 or i == self.cols-1 or j == 0 or j == self.rows-1):
		# 	#self.players.remove()
		# 	return True
		# else:
		# 	return False

	def allPigsEscaped(self):
		for pigId in range(self.numPigs):
			if not self.isEscaped(pigId):
				return False
		return True

	def isCaptured(self, pigId):
		return (optimalPigNextStep(self, pigId) is None and not self.isEscaped(pigId))
			#print "pig captured:", pigId
			#self.players[pigId].isCaptured = True
		# 	return True
		# else:
		# 	return False

	def allPigsCaptured(self):
		for pigId in range(self.numPigs):
			if not self.isCaptured(pigId):
				return False
		return True

	def allPigsEscapedOrCaptued(self):
		for pigId in range(self.numPigs):
			if not self.isEscaped(pigId) and not self.isCaptured(pigId):
				return False
		return True

	def nPigsEscaped(self):
		pigs_escape = 0
		for pigId in range(self.numPigs):
			if self.isEscaped(pigId):
				pigs_escape += 1.

		score = round((pigs_escape / float(self.numPigs)),4)
		return score

	#we are kind of allowing pigs to go over each other 
	def getAlmostLegalMoves(self, pos=None):
		x, y = pos

		#if it is a stone ignore
		if self.fieldIsStone(pos) == -1:
			return []

		moves = []

		#even row 
		if x%2 == 0:
			if x != 0:
				moves.append((x-1,y)) # top right
			if x != self.rows-1:
				moves.append((x+1,y)) # bottom right
			if y != self.cols-1:
				moves.append((x,y+1)) # right
			if y != 0:
				moves.append((x, y-1)) # left
				if x != 0:
					moves.append((x-1,y-1)) # top left
				if x != self.rows - 1:
					moves.append((x+1, y-1)) # bottom left

		#odd row
		else:
			moves.append((x-1,y)) # top left
			if y != 0:
				moves.append((x, y-1)) # left
				if x != self.rows-1:
					moves.append((x+1, y)) # bottom left
			if y != self.cols -1:
				moves.append((x,y+1)) # right
				moves.append((x-1, y+1)) # top right
				if x != self.rows-1:
					moves.append((x+1, y+1)) # bottom right

		# remove all moves *to* stones/blocked fields
		new_moves = []
		for v in moves:
			if self.fieldIsAlmostEmpty(v):
				new_moves.append(v)

		return new_moves
			

	def getLegalMoves(self, pos=None):
		if not pos is None or self.players[self.turn].isPig:
			# get pig's possible moves
			if pos is None:
				pos = self.pigPositions[self.players[self.turn].pigId]
		
			x, y = pos
		
			#if it is a stone ignore
			if self.fieldIsStone(pos) == -1:
				return []

			moves = []

			#even row 
			if x%2 == 0:
				if x != 0:
					moves.append((x-1,y)) # top right
				if x != self.rows-1:
					moves.append((x+1,y)) # bottom right
				if y != self.cols-1:
					moves.append((x,y+1)) # right
				if y != 0:
					moves.append((x, y-1)) # left
					if x != 0:
						moves.append((x-1,y-1)) # top left
					if x != self.rows - 1:
						moves.append((x+1, y-1)) # bottom left

			#odd row
			else:
				moves.append((x-1,y)) # top left
				if y != 0:
					moves.append((x, y-1)) # left
					if x != self.rows-1:
						moves.append((x+1, y)) # bottom left
				if y != self.cols -1:
					moves.append((x,y+1)) # right
					moves.append((x-1, y+1)) # top right
					if x != self.rows-1:
						moves.append((x+1, y+1)) # bottom right

			# remove all moves *to* stones/blocked fields
			new_moves = []
			for v in moves:
				if self.fieldIsEmpty(v):
					new_moves.append(v)

			return new_moves

		else:
			# get all possible stone placements
			moves = []

			for r in range(self.rows):
				for c in range(self.cols):
					if self.grid[r][c] == 0:
						moves.append((r, c)) # can place stone there

			return moves

	def play(self):
		self.players[self.turn].play(self)


	def allNextStoneStates(self):
		nextStates = []
		moves = self.getLegalMoves()
		for move in moves:
				moveGS = deepcopy(self)
				moveGS.placeBlock(move)
				nextStates.append(moveGS)			
		return nextStates


	def allNextStates(self):
		# generate all possible states from all possible moves in getLegalMoves
		nextStates = []
			
		moves = self.getLegalMoves()

		if self.isPigTurn():
			# do each move
			for move in moves:
				moveGS = deepcopy(self)
				moveGS.movePig(move, self.players[self.turn].pigId)
				nextStates.append(moveGS)

		else:
			# do each move
			for move in moves:
				moveGS = deepcopy(self)
				moveGS.placeBlock(move)
				nextStates.append(moveGS)

		return nextStates

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

