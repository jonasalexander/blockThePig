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
		
class minimaxPigAgent(pigAgent):
	def __init__(self):
		super(minimaxPigAgent, self).__init__(self.pigId)
		return

	def play(self, GS):

		return


	