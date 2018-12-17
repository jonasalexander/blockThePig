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
		# print('pigID',pigId)
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
		pigIds = range(GS.numPigs)
		pigzz = []
		for i in pigIds:
			pigzz.append(GS.pigPositions[i])

		nextMoves = GS.allNextStoneStates()

		original_score = 0 
		for pos in pigzz:
			original_score += util.BFS_numerical(GS, pos)

		list_scores = []

		for k in nextMoves:
			# print('grid')
			# for one in k.grid:
				# print(one)

			score = []
			for pos in pigzz:
				score.append(util.BFS_numerical(k, pos))
				# print('score', score)

			list_scores.append((sum(score), k))


		list_scores.sort(key = lambda x:x[0], reverse = True)
		# print(list_scores[0])

		if list_scores[0][0] != original_score:
			_, best_world = list_scores[0]
			best_move = util.diff_between_boards(GS.grid, best_world.grid)
		else:
			for pos in pigIds:
				if GS.isCaptured(pos) or GS.isEscaped(pos):
					continue
				else:
					best_move = util.optimalPigNextStep(GS, pos)


		
		GS.placeBlock(best_move)




			

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
				# if current.GS.isPigTurn():
				# 	compare = 'min'
				# else:
				# 	compare = 'max'
				# current.findBestChild(compare)
				if current.GS.isPigTurn():
				#if(current.simpleDepth%len(GS.players) > 0):
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
		def minValue(GS, d, p, a, b):
			if GS.allPigsEscapedOrCaptued():
				return GS.nPigsEscaped()
			
			v_best = float("inf") 
			v = v_best

			successors = GS.allNextStatesWithMoves()
			#print("Min len legal moves", len(successors))

			for move, successor in successors.items():
				if(p==GS.numPigs):
					if(d == self.maxDepth-1):
						v = heuristics.sumPigDistanceToEdge(successor)
					else:
						v = maxValue(successor, d+1 ,a , b)
				else:
					v = minValue(successor, d, p+1, a, b)

				if v < v_best:
					v_best = v 
				if v_best < a:
					return v_best
				b = min(b, v_best)
			return v_best
				
		def maxValue(GS, d, a, b):
			if GS.allPigsEscapedOrCaptued():
				return GS.nPigsEscaped()
			
			v_best = float("-inf") 
			v = v_best

			successors = GS.allNextStatesWithMoves()
			# print("Stone: Max len legal moves", len(successors))
			
			topAction = successors.keys()[0]

			for move, successor in successors.items():
				v = minValue(successor, d, 1, a, b)
				if v > v_best:
					v_best = v 
					topAction = move

				if v_best > b:
					return v_best 

				a = max(a, v_best)

				if(d == 0):
					return topAction
				else:
					return v_best

		move = maxValue(GS, 0, float("-inf"), float("inf"))
		print("placing stone optimally", move)
		GS.placeBlock(move)

	def play2(self, GS):
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
				# if(current.simpleDepth%len(GS.players) > 0):
				if current.GS.isPigTurn():
					compare = 'min'
				else:
					compare = 'max'
				# current.findBestChild(compare)

				a, b = current.findBestChildPruned(compare, a, b)
				print "Stone", (a, b)

				if current.parent is None:
					break # have finished exploring
				
				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			current = newCurrent
		
		move = root.favoriteChild.GS.lastMove
		print("placing stone optimally", move, "with", root.favoriteChildValue)
		GS.placeBlock(move)


