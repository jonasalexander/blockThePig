import Tkinter as tk

from hexagon import Hexagon, Point
from game_state import GameState

from collections import defaultdict

root = tk.Tk()
root.withdraw() # Make sure no window drawn for root Tk() instance

# Global vars
N_ROWS = 10
N_COLS = 10
STATES = ['free', 'pig', 'block']

# Called when user closes a window.
def cleanUp():
	root.destroy()

def main():

	# Tkinter window config
	window = tk.Toplevel()
	window.title('Block The Pig')
	window.minsize(width=500, height=500)
	window.protocol('WM_DELETE_WINDOW', cleanUp)
	canvas = tk.Canvas(window, width=500, height=500)
	canvas.configure(scrollregion=(0, 0, 400, 400))
	canvas.pack(side="top", fill="both", expand=True)

	# Init game state
	GS = GameState(N_ROWS, N_COLS)
	# print GS.grid


	#TANC's CODE
	#THE FOlLOWING CODE CREATES AN ADJACENCY LIST

	Adjacency_List = defaultdict(list)

	#POPULATE ADJACENCY LIST - you need to change depending whether row is even or odd
	for j, row in enumerate(GS.grid):
		for i, value in enumerate(row):
			edges = []

			#if it is a stone ignore
			if value == -1:
				continue

			#even row 
			if j%2 == 0:
				if i != 0:
					edges.append((i-1,j))
					if j != 0:
						edges.append((i-1, j-1))
					
					if j != N_ROWS - 1:
						edges.append((i-1, j+1 ))

				if i != N_COLS -1:
					edges.append((i+1,j))

				if j != 0:
					edges.append((i, j-1))
				
				if j != N_ROWS - 1:
					edges.append((i, j+1))

			#odd row
			elif j%2 == 1:
				if i != 0:
					edges.append((i-1,j))

				if i != N_COLS -1:

					edges.append((i+1,j))
					
					if j != 0:
						edges.append((i+1, j-1))
					
					if j != N_ROWS - 1:
						edges.append((i+1, j+1 ))

				if j != 0:
					edges.append((i, j-1))
				
				if j != N_ROWS -1:
					edges.append((i, j+1))

			Adjacency_List[(i,j)] = edges

	#you know need to remove all edges that don't actually exist:
	New_Adjacency_List = defaultdict(list)
	for x in Adjacency_List:
		new_edges = []
		edges = Adjacency_List[x]
		for (i,j) in edges:
			# print(i,j)
			if GS.grid[j][i] != -1:
				new_edges.append((i,j))
		New_Adjacency_List[x] = new_edges


	# you now have an adjacnecy table
	

	# you now need to calculate how many moves it will take you to go somewhere

	# the following BFS CAN be improved - the plane landed so dont judge 
	# just created a table with steps you need to leave and rocks are 0 at the moment 
	steps_to_leave = [[0]*N_COLS for i in range(N_ROWS)]
	def bfs(start_node):
		fringe = []
		visited = set()
		depth_tracker = []

		i,j = start_node
		if i == 0 or i == N_COLS-1 or j == 0 or j == N_ROWS-1:
			return 1


		depth = 1
		fringe.append((start_node, depth))
		while fringe != []:
			v, depth = fringe.pop(0)
			visited.add(v)
			# depth_tracker.append((v,d))
			neighbours = New_Adjacency_List[v]
			for node in neighbours:
				if node not in visited:
					fringe.append((node, depth + 1))	

				i,j = node
				if i == 0 or i == N_COLS-1 or j == 0 or j == N_ROWS-1:
					return depth + 1		
			
	for x in New_Adjacency_List:
		i,j = x
		n = bfs(x)
		steps_to_leave[j][i] = n


	# for i in steps_to_leave:
	# 	print(i)



	pig_pos = GS.pigPosition


	# Draw grids
	offset = Hexagon.sideLength*1.1
	for row in range(N_ROWS):
		for col in range(N_COLS):
			y = offset+row*Hexagon.sideLength*1.5
			if row%2 == 0:
				x = offset+col*Hexagon.sideLength*3**(0.5)
			else:
				x = offset+(col+0.5)*Hexagon.sideLength*3**(0.5)
			Hexagon(canvas, Point(x, y), STATES[GS.grid[row][col]])

	root.mainloop()




	

if __name__ == '__main__':
	main()