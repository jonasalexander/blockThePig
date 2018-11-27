from util import *

class pigAgent(object):

	def __init__(self, pigId):
		self.pigId = pigId
		return

	def play(self):
		return


class simplePigAgent(pigAgent):

	def __init__(self, pigId):
		super(simplePigAgent, self).__init__(pigId)
		return

	def play(self, GS):

		move = optimalPigNextStep(GS, self.pigId)

		if move is None:
			if not GS.isEscaped(self.pigId):
				print 'Pig unexpectedly can not find any next move'
			return

		GS.movePig(move, self.pigId)
		
class minimaxPigAgent(pigAgent):
	def __init__(self):
		return

	def play(self, GS):

		return


	