from util import *
from minimaxNode import minimaxNode
import heuristics
import random

class pigAgent(object):

	def __init__(self, pigId):
		self.pigId = pigId
		self.isPig = True
		self.isEscaped = False
		self.isCaptured = False
		return

	def play(self):
		return

class rrandomPigAgent(pigAgent):
	def __init__(self, pigId):
		super(rrandomPigAgent, self).__init__(pigId)
		return

	def play(self, GS):
		if GS.isEscaped(self.pigId) or GS.isCaptured(self.pigId):
			print ("captured", self.pigId, "SKIP")
			GS.incrementTurn()
			return
		
		moves = GS.getLegalMoves()
		best_move = random.choice(moves)
		GS.movePig(best_move, self.pigId)


class simplePigAgent(pigAgent):

	def __init__(self, pigId):
		super(simplePigAgent, self).__init__(pigId)
		return

	def play(self, GS):

		if GS.isEscaped(self.pigId) or GS.isCaptured(self.pigId):
			# if(GS.isEscaped(self.pigId)):
			# 	#GS.players.remove(self)
			# 	x, y = GS.pigPositions[self.pigId]
			# 	GS.grid[x][y] = 0
			print ("captured", self.pigId, "SKIP")
			GS.incrementTurn()
			return

		move = optimalPigNextStep(GS, self.pigId)

		if move is None:
			if not GS.isEscaped(self.pigId) or GS.isCaptured(self.pigId):
				print ('Pig unexpectedly can not find any next move')
			GS.incrementTurn()
			return

		GS.movePig(move, self.pigId)


#at the momeny just copied part of stone agent to pig agent
class minimaxPigAgent(pigAgent):

	defaultDepth = 1


	def __init__(self, pigId, maxDepth = None):
		if maxDepth is None:
			maxDepth = minimaxPigAgent.defaultDepth
		self.maxDepth = maxDepth
		super(minimaxPigAgent, self).__init__(pigId)


	def play(self, GS):
		if GS.isEscaped(self.pigId) or GS.isCaptured(self.pigId):
			# if(GS.isEscaped(self.pigId)):
			# 	#GS.players.remove(self)
			# 	x, y = GS.pigPositions[self.pigId]
			# 	GS.grid[x][y] = 0
			print ("captured", self.pigId, "SKIP")
			GS.incrementTurn()
			return

		root = minimaxNode(GS, None)
		current = root

		while True:
			if current is None:
				break

			if current.simpleDepth >= self.maxDepth*len(GS.players):
				# we're at max depth
				# so just evaluate with heuristic 
				# and move on to sibling node

				#TODO: THIS IS WHERE WE CAN MAKE PIGS INDIVIDUAL AGENTS, just look at thir own distance?
				current.favoriteChildValue = heuristics.sumPigDistanceToEdge(current.GS)
				if current.parent is None:
					break # have finished exploring

				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			else:
				# expand child nodes
				current.addChildren(current.GS.allNextStates())
				newCurrent = current.nextNode() # get next child (down a level)

			# no more children of this node left to explore
			while newCurrent is None:
				# print "current.simpledepth", current.simpleDepth
				#print "len(GS.players)", len(GS.players)
				# find favorite child for subtree we're done with
				if current.GS.isPigTurn():
				#if(current.simpleDepth%len(GS.players) < GS.numPigs):
					#print "in pigAgent, is pigTurn"
					compare = 'min'
				else:
					#print "in pigAgent, is stoneTurn"
					compare = 'max'

				current.findBestChild(compare)

				if current.parent is None:
					break # have finished exploring
				
				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			current = newCurrent
		
		move = root.favoriteChild.GS.lastMove
		print("moving", self.pigId, "from", GS.pigPositions[self.pigId], "to", move, "root:", root.favoriteChildValue)
		GS.movePig(move, self.pigId)

		# while True
		# 	if current is None:
		# 		break 

		# 				if current.simpleDepth >= self.maxDepth*len(GS.players):
		# 		# we're at max depth
		# 		# so just evaluate with heuristic 
		# 		# and move on to sibling node
		# 		current.favoriteChildValue = heuristics.sumPigDistanceToEdge(current.GS)
		# 		if current.parent is None:
		# 			break # have finished exploring


		#return

class alphaBetaPigAgent(pigAgent):

	defaultDepth = 2

	def __init__(self, pigId, maxDepth = None):
		if maxDepth is None:
			maxDepth = alphaBetaPigAgent.defaultDepth
		self.maxDepth = maxDepth
		super(alphaBetaPigAgent, self).__init__(pigId)

	def play(self, GS):
		if GS.isEscaped(self.pigId) or GS.isCaptured(self.pigId):
			# if(GS.isEscaped(self.pigId)):
			# 	#GS.players.remove(self)
			# 	x, y = GS.pigPositions[self.pigId]
			# 	GS.grid[x][y] = 0
			GS.incrementTurn()
			return

		def minValue(GS, d, p, a, b):
			if GS.allPigsEscapedOrCaptued():
				return GS.nPigsEscaped()
			
			v_best = float("inf") 
			v = v_best

			successors = GS.allNextStatesWithMoves()
			if len(successors) == 0:
				return GS.nPigsEscaped()

			topAction = successors.keys()[0]

			for move, successor in successors.items():
				if(p==GS.numPigs):
					if(d == self.maxDepth-1):
						v = heuristics.sumPigDistanceToEdge(successor)
					else:
						v = maxValue(successor, d ,a , b)
				else:
					v = minValue(successor, d, p+1, a, b)

				if v < v_best:
					v_best = v 
					topAction = move
				if v_best < a:
					return v_best
				b = min(b, v_best)

			if(d == 0):
				return topAction
			else:
				return v_best 
				
		def maxValue(GS, d, a, b):
			if GS.allPigsEscapedOrCaptued():
				return GS.nPigsEscaped()
			
			v_best = float("-inf") 
			v = v_best

			successors = GS.allNextStatesWithMoves()
			# print("Pig: Max len legal moves", len(successors))

			for move, successor in successors.items():
				v = minValue(successor, d+1, 1, a, b)
				if v > v_best:
					v_best = v 

				if v_best > b:
					return v_best 

				a = max(a, v_best)

			return v_best 

		move = minValue(GS, 0, 1, float("-inf"), float("inf"))
		print("moving", self.pigId, "from", GS.pigPositions[self.pigId], "to", move)
		GS.movePig(move, self.pigId)

	def play2(self, GS):
		if GS.isEscaped(self.pigId) or GS.isCaptured(self.pigId):
			# if(GS.isEscaped(self.pigId)):
			# 	#GS.players.remove(self)
			# 	x, y = GS.pigPositions[self.pigId]
			# 	GS.grid[x][y] = 0
			GS.incrementTurn()
			return
		root = minimaxNode(GS, None)
		current = root
		a =float("-inf")
		b=float("inf")

		while True:
			if current is None:
				break

			if current.simpleDepth >= self.maxDepth*len(GS.players):
				# we're at max depth
				# so just evaluate with heuristic 
				# and move on to sibling node
				current.favoriteChildValue = heuristics.sumPigDistanceToEdge(current.GS)
				if current.parent is None:
					break # have finished exploring

				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			else:
				# expand child nodes
				current.addChildren(current.GS.allNextStates())
				newCurrent = current.nextNode() # get next child (down a level)

			# no more children of this node left to explore
			while newCurrent is None:
				# find favorite child for subtree we're done with
				if current.GS.isPigTurn():
				# if(current.simpleDepth%len(GS.players) < GS.numPigs):
					compare = 'min'
				else:
					compare = 'max'

				a, b = current.findBestChildPruned(compare, a, b)
				print "Pig", (a, b)

				if current.parent is None:
					break # have finished exploring
				
				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			current = newCurrent
		
		move = root.favoriteChild.GS.lastMove
		print("moving", self.pigId, "from", GS.pigPositions[self.pigId], "to", move, "with", root.favoriteChildValue)
		GS.movePig(move, self.pigId)

	