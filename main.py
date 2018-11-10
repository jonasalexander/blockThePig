import Tkinter as tk

from hexagon import Hexagon, Point
from game_state import GameState

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
	print GS.grid

	# Draw grid
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