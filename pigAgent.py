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

		adjacencyList = getAdjacencyList(GS)

		# Use BFS/Djikstra to figure out next step
		fringe = []
		visited = set()
		parent = {}

		i,j = GS.pigPosition
		if i == 0 or i == N_COLS-1 or j == 0 or j == N_ROWS-1:
			return 1

		final = None
		fringe.append(GS.pigPosition)
		while fringe:
			print 'fringe: ' + str(fringe)
			#v = fringe.pop(0)
			vx, vy = fringe.pop(0)
			#don't expand paths that go through stones, still finicky on diagonals
			while GS.grid[vx][vy] < 0:
				vx, vy = fringe.pop(0)
			visited.add((vx, vy)) 
			neighbours = adjacencyList[(vx, vy)]
			#print neighbours
			for node in neighbours:
				if node not in visited:
					parent[node] = (vx, vy)
					fringe.append(node)
					i, j = node
					#print 'node: ' + str(node)
					if i == 0 or i == N_COLS-1 or j == 0 or j == N_ROWS-1:
						#print 'isGoal'
						fringe = []
						final = node
						break

		if final is None:
			print 'No way for pig to escape!'
			return
		print parent
		next = parent[final]
		while next != GS.pigPosition:
			next, final = parent[next], next

		print "PIG:", (final[0], final[1])
		GS.movePig(final[0], final[1])
		

			


	