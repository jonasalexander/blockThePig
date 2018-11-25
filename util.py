from collections import defaultdict

# Global vars
N_ROWS = 10
N_COLS = 10
STATES = ['free', 'pig', 'block']

def getAdjacencyList(GS):
	# Creates an adjacency list
	adjacencyList = defaultdict(list)

	# Populate adjacency list 
	# need to change depending whether row is even or odd
	for x, row in enumerate(GS.grid):
		for y, value in enumerate(row):
			edges = []

			#if it is a stone ignore
			if value == -1:
				continue

			#even row 
			if x%2 == 0:
				if x != 0:
					edges.append((x-1,y))
					if y != N_ROWS - 1:
						edges.append((x-1, y+1))

				if y != N_COLS-1:
					edges.append((x,y+1))

				if y != 0:
					edges.append((x, y-1))

				if x != N_ROWS-1:
					edges.append((x+1,y))
					if y != N_ROWS - 1:
						edges.append((x+1, y+1))

			#odd row
			else:
				edges.append((x-1,y))

				if x != N_ROWS-1:
					edges.append((x+1,y))

				if y != N_COLS -1:
					edges.append((x, y+1))

				if y != 0:
					edges.append((x, y-1))
					edges.append((x-1, y-1))

					if x != N_ROWS-1:
						edges.append((x-1, y-1))

			# remove all edges to stones/blocked fields
			new_edges = []
			for i,j in edges:
				if GS.grid[i][j] != -1:
					new_edges.append((i,j))

			adjacencyList[(x,y)] = new_edges

	return adjacencyList