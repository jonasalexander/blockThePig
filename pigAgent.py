from util import *

class pigAgent():

	def __init__(self):
		return

	def play(self):
		return


class simplePigAgent(pigAgent):

	def __init__(self):
		return

	def play(self, GS):

		move = optimalPigNextStep(GS)

		if move is None:
			print 'Pig can not find any next move'
			return

		GS.movePig(move)
		
class minimaxPigAgent(pigAgent):
	def __init__(self):
		return

	def play(self, GS):

		return


	