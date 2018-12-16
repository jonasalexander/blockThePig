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

	v_old = 0

	while fringe:
		v = fringe.pop(0)
		if v == None:
			level += 1
			fringe.append(None)
			if v_old == None:
				print('escaping loop of death', location, fringe)
				return(level + 3)
			else:
				v_old = None
		else:
			v_old = v 
			i,j = v
			if i == 0 or i == GS.cols-1 or j == 0 or j == GS.rows-1:
				return 0 

			visited.add(v) 
			neighbours = GS.getAlmostLegalMoves(v)
			for node in neighbours:
				if node not in visited:
					fringe.append(node)
					visited.add(node)
					i, j = node
					if i == 0 or i == GS.cols-1 or j == 0 or j == GS.rows-1:
						return level 


def diff_between_boards(grid1, grid2):
	counter_outer = 0
	for i,j in zip(grid1, grid2):
		counter_inner = 0
		for k,l in zip(i,j):
			if k != l:
				return(counter_outer, counter_inner)
			counter_inner += 1
		
		counter_outer += 1
	
	raise Exception('boards are the same')






