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


class complexStoneAgent(stoneAgent):

	def __init__(self):
		super(complexStoneAgent, self).__init__()
		return

	
	def play(self, GS):
		print('ENTER PLAY')
		pigIds = range(GS.numPigs)


		# get all neighbours of pigs. 
		real_neighbours = []
		for i in pigIds:
			neighbours = GS.getLegalMoves(GS.pigPositions[i])
			real_neighbours += neighbours

		real_neighbours.sort(key=lambda x:x[0]) 

		normal_scores = []
		for n in real_neighbours:
			normal_scores.append(util.BFS_numerical(GS, n))
		
		
		# print(real_neighbours)
		nextMoves = GS.allNextStoneStates()
		# print('NM', nextMoves)
		list_scores = []
		for k in nextMoves:
			print('GRID', )
			for i in k.grid:
				print(i)
			score = []
			for j, x in enumerate(real_neighbours):
				if k.fieldIsStone(x):
					score.append(normal_scores[j] + 1)
				else:
					# print('called')
					score.append(util.BFS_numerical(k, x))

			list_scores.append((sum(score),x))
		
		


		list_scores.sort(key = lambda x:x[0], reverse = True)
		print('list_scores', list_scores)
		sc, move = list_scores[0]

		GS.placeBlock(move)




			

		#get a list of all xy of 6 around make sure they are valid - double count on purpose. 

		# once we have that iterate through all places you can move a stonek keeping a max stone
		
		

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
				if current.GS.isPigTurn():
					compare = 'min'
				else:
					compare = 'max'
				current.findBestChild(compare)

				if current.parent is None:
					break # have finished exploring
				
				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			current = newCurrent
		
		move = root.favoriteChild.GS.lastMove
		GS.placeBlock(move)


