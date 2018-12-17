from util import *
from minimaxNode import minimaxNode
import heuristics

class pigAgent(object):

	def __init__(self, pigId):
		self.pigId = pigId
		self.isPig = True
		self.isEscaped = False
		self.isCaptured = False
		return

	def play(self):
		return


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
				#if current.GS.isPigTurn():
				#print current.simpleDepth
				if(current.simpleDepth%len(GS.players) < GS.numPigs):
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
		print("moving", self.pigId, "from", GS.pigPositions[self.pigId], "to", move, "with", root.favoriteChildValue)
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
				# if current.GS.isPigTurn():
				# 	compare = 'min'
				# else:
				# 	compare = 'max'
				# current.findBestChild(compare)
				#print ("simple depth", current.simpleDepth)
				if(current.simpleDepth%len(GS.players) < GS.numPigs):
					#print "in stoneAgent, is pigTurn"
					compare = 'min'
				else:
					#print "in stoneAgent, is stoneTurn"
					compare = 'max'
				current.findBestChildPruned(compare, float("-inf"), float("-inf"))

				if current.parent is None:
					break # have finished exploring
				
				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			current = newCurrent
		
		move = root.favoriteChild.GS.lastMove
		print("moving", self.pigId, "from", GS.pigPositions[self.pigId], "to", move, "with", root.favoriteChildValue)
		GS.movePig(move, self.pigId)

	