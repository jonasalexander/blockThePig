import Tkinter as tk

from util import *
from hexagon import Hexagon, Point
from gameState import GameState
import pigAgent
import stoneAgent

root = tk.Tk()
root.withdraw() # Make sure no window drawn for root Tk() instance

# Called when user closes a window.
def cleanUp():
	root.destroy()

def main():

	# Tkinter window config
	window = tk.Toplevel()
	window.title('Block The Pig')
	window.minsize(width=500, height=500)
	window.protocol('WM_DELETE_WINDOW', cleanUp)

	# Init game state
	GS = GameState(N_ROWS, N_COLS)

	# Draw window
	GS.draw(window)

	# Simple Pig Agent Gameplay (no placing rocks)
	

	def update():
		if GS.isEscaped():
			print 'Pig escaped!'
			return
		if(GS.pigTurn):
			a = pigAgent.simplePigAgent()
		else:
			a = stoneAgent.simpleStoneAgent()
		a.play(GS)
		#switch player
		GS.pigTurn = not GS.pigTurn
		print GS.pigPosition
		GS.draw(window)
		root.after(1000, update)

	root.after(1000, update)

	root.mainloop()
		
		
		



	

if __name__ == '__main__':
	main()