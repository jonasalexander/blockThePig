from util import *

def sumPigDistanceToEdge(GS):
	# calculate the sum of all pigs' distances to the edge
	# stoneAgent will want to maximize this
	
	s = 0
	for pigId in range(GS.numPigs):
		if GS.isCaptured(pigId):
			s += GS.cols+GS.rows
			continue
		if GS.isEscaped(pigId):
			continue
		s += len(BFSPathToEdge(GS, pigId))
	
	return s

def TancHeuristic(GS):
	s = 0
	for pigId in range(GS.numPigs):
		if GS.isCaptured(pigId):
			s += GS.cols+GS.rows
			continue
		if GS.isEscaped(pigId):
			continue
		s += len(BFS_numerical(GS, GS.pigPostions[pigId]))
	
	return s

# 	#moves = GS.getLegalMoves(self,)
# 	#put a block and check how pig is influenced... 