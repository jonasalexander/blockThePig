import random

import util
import heuristics
from minimaxNode import minimaxNode

class stoneAgent(object):

	def __init__(self):
		self.isPig = False
		return

	def play(self):
		return

class simpleStoneAgent(stoneAgent):

	def __init__(self):
		super(simpleStoneAgent, self).__init__()
		return

	def play(self, GS):

		pigId = random.randint(0, GS.numPigs-1)
		print('pigID',pigId)
		while GS.isEscaped(pigId) or GS.isCaptured(pigId):
			# choose a different pig
			pigId = random.randint(0, GS.numPigs-1) 

		move = util.optimalPigNextStep(GS, pigId)

		if move is None:
			GS.incrementTurn()
			print ('Pig can not find any next move')
			return

		GS.placeBlock(move)


# class complexStoneAgent(stoneAgent):

# 	def __init__(self):
# 		super(simpleStoneAgent, self).__init()
# 		return

# 	def play(self, GS):
		

class minimaxStoneAgent(stoneAgent):

	defaultDepth = 2

	def __init__(self, maxDepth = None):
		if maxDepth is None:
			maxDepth = minimaxStoneAgent.defaultDepth
		self.maxDepth = maxDepth
		super(minimaxStoneAgent, self).__init__()


	def play(self, GS):
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
				if(current.simpleDepth%len(GS.players) > 0):
					#print "in stoneAgent, is pigTurn"
					compare = 'min'
				else:
					#print "in stoneAgent, is stoneTurn"
					compare = 'max'
				current.findBestChild(compare)

				if current.parent is None:
					break # have finished exploring
				
				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			current = newCurrent
		
		move = root.favoriteChild.GS.lastMove
		print("placing stone optimally", move, "with", root.favoriteChildValue)
		GS.placeBlock(move)

class alphaBetaStoneAgent(stoneAgent):

	defaultDepth = 2

	def __init__(self, maxDepth = None):
		if maxDepth is None:
			maxDepth = alphaBetaStoneAgent.defaultDepth
		self.maxDepth = maxDepth
		super(alphaBetaStoneAgent, self).__init__()


	def play(self, GS):
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
				if(current.simpleDepth%len(GS.players) > 0):
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
		print("placing stone optimally", move, "with", root.favoriteChildValue)
		GS.placeBlock(move)


