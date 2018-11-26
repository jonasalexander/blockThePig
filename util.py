from collections import defaultdict

# Global vars
N_ROWS = 10
N_COLS = 10
STATES = ['free', 'pig', 'block']

def optimalPigNextStep(GS):
	# Use BFS/Djikstra to figure out next step
	fringe = []
	visited = set()
	parent = {}

	i,j = GS.pigPosition
	if i == 0 or i == GS.cols-1 or j == 0 or j == GS.rows-1:
		return 1

	final = None
	fringe.append(GS.pigPosition)
	while fringe:
		v = fringe.pop(0)
		visited.add(v) 
		neighbours = GS.getLegalMoves(v)
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
	
	next = parent[final]
	while next != GS.pigPosition:
		next, final = parent[next], next

	return final