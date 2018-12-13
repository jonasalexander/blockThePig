import tkinter as tk
import argparse

from util import *
from hexagon import Hexagon, Point
from gameState import GameState
import pigAgent
import stoneAgent

root = tk.Tk()
root.withdraw() # Make sure no window drawn for root Tk() instance
pigWins = 0

# Called when user closes a window.
def cleanUp():
	root.destroy()

def main(gameType, numStoneAgents, numPigAgents, maxDepth=None):
	global pigWins
	# Tkinter window config
	window = tk.Toplevel()
	window.title('Block The Pig')
	window.minsize(width=500, height=500)
	window.protocol('WM_DELETE_WINDOW', cleanUp)

	# Simple Pig Agent Gameplay
	if gameType == 'simple':

		# will iterate through players for turns
		players = [pigAgent.simplePigAgent(i) for i in range(numPigAgents)] + [stoneAgent.simpleStoneAgent() for _ in range(numStoneAgents)]

		# Init game state
		GS = GameState(N_ROWS, N_COLS, players, numPigs=numPigAgents)

		# Draw window
		GS.draw(window)

		def update():
			if GS.allPigsEscaped():
				print ('All pigs escaped!')
				cleanUp()
				pigWins += 1
				return 
			
			if GS.allPigsCaptured():
				print ('All pigs captured!')
				cleanUp()
				return 

			elif GS.allPigsEscapedOrCaptued():
				print ('All pigs either escaped or captured!')
				cleanUp()
				pigWins += 1
				return 
			
			GS.play() # where the magic happens
			GS.draw(window)
			root.after(TIME_DELAY, update)

		root.after(TIME_DELAY, update)

	# Mini-max Agent Gameplay
	elif gameType == 'minimax':

		# will iterate through players for turns
		players = [pigAgent.simplePigAgent(i) for i in range(numPigAgents)] + [stoneAgent.minimaxStoneAgent(maxDepth) for _ in range(numStoneAgents)]

		# Init game state
		GS = GameState(N_ROWS, N_COLS, players, numPigs=numPigAgents)

		# Draw window
		GS.draw(window)

		def update():
			if GS.allPigsEscaped():
				print ('All pigs escaped!')
				cleanUp()
				pigWins += 1
				return 
			
			if GS.allPigsCaptured():
				print ('All pigs captured!')
				cleanUp()
				return 
			
			GS.play() # where the magic happens
			GS.draw(window)
			root.after(TIME_DELAY, update)

		root.after(TIME_DELAY, update)

	root.mainloop()
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	# Optional Arguments
	parser.add_argument('-ns', help='Number of stone agents.', dest='numStoneAgents', default=1, type=int)
	parser.add_argument('-np', help='Number of pig agents.', dest='numPigAgents', default=1, type=int)

	parser.add_argument('-s', help='Play simple game.', dest='simpleGame', action='store_true')
	parser.add_argument('-m', help='Play minimax game.', dest='minimax', action='store_true')
	parser.add_argument('-d', help='If minimax game, the depth of the states the agents should explore.', dest='maxDepth',  default=None, type=int)
	parser.add_argument('-n', help='Number of games to simulare', dest='iterations', type = int, default = 1)


	args = parser.parse_args()

	if args.simpleGame:
		for n in range(args.iterations):
			main('simple', args.numStoneAgents, args.numPigAgents)
	elif args.minimax:
		for n in range(args.iterations):
			main('minimax', args.numStoneAgents, args.numPigAgents, args.maxDepth)
			print ("pig wins at", n, ":", pigWins)
	print ('pig win rate:', pigWins/args.iterations)

