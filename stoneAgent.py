from util import *

class stoneAgent():

	def __init__(self):
		return

	def play(self):
		return


class simpleStoneAgent(stoneAgent):

	def __init__(self):
		return

	def play(self, GS):

		move = optimalPigNextStep(GS)

		if move is None:
			print 'Pig can not find any next move'
			return

		GS.placeBlock(move)

class minimaxStoneAgent(stoneAgent):

	def __init__(self):
		return

	def play(self, GS):

		return