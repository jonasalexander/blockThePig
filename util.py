from copy import deepcopy

# Global vars
N_ROWS = 6
N_COLS = 6
STATES = ['free', 'pig', 'block']
MAXDEPTH = 8
TIME_DELAY = 500


# def beststone(GS):	
# 	for i in GS.
# 	i,j = GS.pigPositions[pigID]

def BFSPathToEdge(GS, pigId):
	# Use BFS/Djikstra to figure out path
	fringe = []
	visited = set()
	parent = {}

	i,j = GS.pigPositions[pigId]
	if i == 0 or i == GS.cols-1 or j == 0 or j == GS.rows-1:
		return

	final = None
	fringe.append(GS.pigPositions[pigId])
	while fringe:
		v = fringe.pop(0)
		visited.add(v) 
		neighbours = GS.getLegalMoves(pos=v)
		for node in neighbours:
			if node not in visited and GS.fieldIsEmpty(node):
				parent[node] = v
				fringe.append(node)
				visited.add(node)
				i, j = node
				if i == 0 or i == GS.cols-1 or j == 0 or j == GS.rows-1:
					fringe = []
					final = node
					break

	if final is None:
		return
	
	path = [final, parent[final]]
	next = parent[final]
	while next != GS.pigPositions[pigId]:
		next, final = parent[next], next
		path.append(next)

	return path[::-1]

def BFSPath(GS, pigId, goal):
	# Use BFS/Djikstra to figure out path
	fringe = []
	visited = set()
	parent = {}

	i,j = GS.pigPositions[pigId]
	if (i, j) == goal:
		return

	final = None
	fringe.append(GS.pigPositions[pigId])
	while fringe:
		v = fringe.pop(0)
		visited.add(v) 
		neighbours = GS.getLegalMoves(pos=v)
		for node in neighbours:
			if node not in visited and GS.fieldIsEmpty(node):
				parent[node] = v
				fringe.append(node)
				visited.add(node)
				if node == goal:
					fringe = []
					final = node
					break

	if final is None:
		return
	
	path = [final, parent[final]]
	next = parent[final]
	while next != GS.pigPositions[pigId]:
		next, final = parent[next], next
		path.append(next)

	return path[::-1]

def optimalPigNextStep(GS, pigId):
	path = BFSPathToEdge(GS, pigId)
	if path is None:
		return
	return path[1]


def BFS_numerical(GS, location):
	# Use BFS/Djikstra to figure out path
	fringe = []
	visited = set()
	visited.add(location)
	level = 1

	fringe.append(location)
	fringe.append(None)
	while fringe:
		v = fringe.pop(0)
		if v == None:
			# print('level')
			level += 1
			fringe.append(None)
			continue

		else:
			i,j = v
			if i == 0 or i == GS.cols-1 or j == 0 or j == GS.rows-1:
				return 0 

			visited.add(v) 
			neighbours = GS.getAlmostLegalMoves(v)
			for node in neighbours:
				# print('inside', 'v', v, 'n', node,  neighbours)
				if node not in visited:
					fringe.append(node)
					visited.add(node)
					i, j = node
					if i == 0 or i == GS.cols-1 or j == 0 or j == GS.rows-1:
						return level 






