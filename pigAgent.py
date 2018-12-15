from util import *

class pigAgent(object):

	def __init__(self, pigId):
		self.pigId = pigId
		self.isPig = True
		return

	def play(self):
		return


class simplePigAgent(pigAgent):

	def __init__(self, pigId):
		super(simplePigAgent, self).__init__(pigId)
		return

	def play(self, GS):

		if GS.isEscaped(self.pigId) or GS.isCaptured(self.pigId):
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


	def __init__(self):
		if  maxDepth is None:
			maxDepth = minimaxPigAgent.defaultDepth

		self.maxDepth = maxDepth  
		super(minimaxPigAgent, self).__init__(pigId)

		return 

	def play(self, GS):
		root = minimaxNode(GS, None)
		current = root

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


		return


	