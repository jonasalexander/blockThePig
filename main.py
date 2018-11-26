import Tkinter as tk
import argparse

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

def main(gameType, numStoneAgents):

	# Tkinter window config
	window = tk.Toplevel()
	window.title('Block The Pig')
	window.minsize(width=500, height=500)
	window.protocol('WM_DELETE_WINDOW', cleanUp)

	# Init game state
	GS = GameState(N_ROWS, N_COLS)

	# Draw window
	GS.draw(window)

	# Simple Pig Agent Gameplay
	if gameType == 'simple':
		def update(players, turn):
			if GS.isEscaped():
				print 'Pig escaped!'
				return
			
			if GS.isCaptured():
				print 'Pig is captured'
				return
			
			players[turn].play(GS)
			# switch player
			turn += 1
			turn = turn%len(players)
			
			GS.draw(window)
			root.after(1000, update, players, turn)

		players = [pigAgent.simplePigAgent()] + [stoneAgent.simpleStoneAgent() for _ in range(numStoneAgents)]
		root.after(1000, update, players, 0)

	# Mini-max Agents
	if gameType == 'minimax':
		def update(players, turn):
			if GS.isEscaped():
				print 'Pig escaped!'
				return
			
			if GS.isCaptured():
				print 'Pig is captured'
				return
			
			players[turn].play(GS)
			# switch player
			turn += 1
			turn = turn%len(players)
			
			GS.draw(window)
			root.after(1000, update, players, turn)

		players = [pigAgent.minimaxPigAgent()] + [stoneAgent.minimaxStoneAgent() for _ in range(numStoneAgents)]
		root.after(1000, update, players, 0)

	root.mainloop()
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	# Optional Arguments
	parser.add_argument('-p', help='Number of stone agents.', dest='numStoneAgents', default=1, type=int)

	parser.add_argument('-s', help='Play simple game.', dest='simpleGame', action='store_true')
	parser.add_argument('-m', help='Play minimax game.', dest='minimax', action='store_true')

	args = parser.parse_args()

	if args.simpleGame:
		main('simple', args.numStoneAgents)
	elif args.minimax:
		main('minimax', args.numStoneAgents)

