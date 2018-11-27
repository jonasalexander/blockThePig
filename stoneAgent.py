import random

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

		pigId = random.randint(0, GS.numPigs-1)
		while GS.isEscaped(pigId) or GS.isCaptured(pigId):
			pigId = random.randint(0, GS.numPigs-1)

		move = optimalPigNextStep(GS, pigId)

		if move is None:
			print 'Pig can not find any next move'
			return

		GS.placeBlock(move)

class minimaxStoneAgent(stoneAgent):

	def __init__(self):
		return

	def play(self, GS):

		return