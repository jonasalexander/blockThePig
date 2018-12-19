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
	

class rrandomStoneAgent(stoneAgent):

	def __init__(self):
		super(rrandomStoneAgent, self).__init__()
		return

	def play(self, GS):
		nextMoves = GS.allNextStoneStates()
		movezz = random.choice(nextMoves)
		best_move = util.diff_between_boards(GS.grid, movezz.grid)
		GS.placeBlock(best_move)


class simpleStoneAgent(stoneAgent):

	def play(self, GS):

		pigId = random.randint(0, GS.numPigs-1)
		while GS.isEscaped(pigId) or GS.isCaptured(pigId):
			# choose a different pig
			pigId = random.randint(0, GS.numPigs-1) 

		move = util.optimalPigNextStep(GS, pigId)

		if move is None:
			GS.incrementTurn()
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
			score = []
			for pos, ids in zip(pigzz, pigIds):
				if GS.isCaptured(ids) or GS.isEscaped(ids):
					continue

				score.append(util.BFS_numerical(k, pos))

			list_scores.append((sum(score), k))

		list_scores.sort(key = lambda x:x[0], reverse = True)

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

		# once we have that iterate through all places you can move a stone keeping a max stone
		
class minimaxStoneAgent(stoneAgent):
	defaultDepth = 1

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
				current.favoriteChildValue = -1*heuristics.sumPigDistanceToEdge(current.GS)
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

class alphaBetaStoneAgent(stoneAgent):

	defaultDepth = 1

	def __init__(self, maxDepth = None):
		if maxDepth is None:
			maxDepth = alphaBetaStoneAgent.defaultDepth
		self.maxDepth = maxDepth
		super(alphaBetaStoneAgent, self).__init__()

	#adapted from P2 multiagents.py
	def play(self, GS):
		def tiebreak(actions):
			bestDist = float("inf")
			tiebreaker = []
			for option in actions:
				# option is a coordinate
				newDist = GS.distanceToNearestPig(option)
				if (newDist < bestDist):
					bestDist = newDist
					tiebreaker = [option]
				elif newDist == bestDist:
					tiebreaker.append(option)
			r = random.randint(0, len(tiebreaker)-1)
			return tiebreaker[r]

		def minValue(GS, d, p, a, b):
			if GS.allPigsEscapedOrCaptued():
				return GS.nPigsEscaped()
			
			v_best = float("inf") 
			v = v_best

			successors = GS.allNextStatesWithMoves()

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
			
			topAction = []

			for action, successor in successors.items():
				v = minValue(successor, d, 1, a, b)
				if v >= v_best:
					v_best = v 
					topAction.append(action)

				if v_best > b:
					return v_best 

				a = max(a, v_best)

			if(d == 0):
				if (len(topAction) > 1):
					return tiebreak(topAction)
				else: return topAction[0]
			else:
				return v_best

		move = maxValue(GS, 0, float("-inf"), float("inf"))
		GS.placeBlock(move)

	def playOriginal(self, GS):
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
					compare = 'min'
				else:
					compare = 'max'
				current.findBestChild(compare)

				a, b = current.findBestChildPruned(compare, a, b)

				if current.parent is None:
					break # have finished exploring
				
				# recurse up the tree
				current = current.parent
				newCurrent = current.nextNode()

			current = newCurrent
		
		move = root.favoriteChild.GS.lastMove
		GS.placeBlock(move)


