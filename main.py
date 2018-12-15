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
	try:
		root.quit()
	except:
		pass

def main(gameType, numStoneAgents, numPigAgents, maxDepth=None, quiet=False):

	# will iterate through players for turns
	if(gameType=="simple"):
		players = [pigAgent.simplePigAgent(i) for i in range(numPigAgents)] + [stoneAgent.minimaxStoneAgent(maxDepth) for _ in range(numStoneAgents)]
	elif(gameType=="minimax"):
		players = [pigAgent.simplePigAgent(i) for i in range(numPigAgents)] + [stoneAgent.simpleStoneAgent() for _ in range(numStoneAgents)]

	# Init game state
	GS = GameState(N_ROWS, N_COLS, players, numPigs=numPigAgents, quiet=quiet)
	# Tkinter window config
	if(not quiet):
		window = tk.Toplevel()
		window.title('Block The Pig')
		window.minsize(width=500, height=500)
		window.protocol('WM_DELETE_WINDOW', cleanUp)


	# Simple Pig Agent Gameplay
	if gameType == 'simple':

		# Draw window
		if(not quiet):
			GS.draw(window)

		def update():
			if GS.allPigsEscaped() or GS.allPigsCaptured() or GS.allPigsEscapedOrCaptued():
				print ('Game ended')
				if(not quiet):
					cleanUp()
				return True

			GS.play() # where the magic happens
			if(not quiet):
				GS.draw(window)
				root.after(TIME_DELAY, update)
			else:
				return update()

		if(not quiet):
			root.after(TIME_DELAY, update)
		else:
			return update()

	# Mini-max Agent Gameplay
	elif gameType == 'minimax':
		print(quiet)
		# # will iterate through players for turns
		# players = [pigAgent.simplePigAgent(i) for i in range(numPigAgents)] + [stoneAgent.minimaxStoneAgent(maxDepth) for _ in range(numStoneAgents)]

		# # Init game state
		# GS = GameState(N_ROWS, N_COLS, players, numPigs=numPigAgents)

		# Draw window
		if(not quiet):
			GS.draw(window)

		def update():
			if GS.allPigsEscaped():
				print ('All pigs escaped!')
				if(not quiet):
					cleanUp()
				return True
			
			if GS.allPigsCaptured():
				print ('All pigs captured!')
				if(not quiet):
					cleanUp()
				return False
			
			GS.play() # where the magic happens
			if(not quiet):
				GS.draw(window)
				root.after(TIME_DELAY, update)
			else: 
				return update()

		if(not quiet):
			root.after(TIME_DELAY, update)
		else: 
			return update()

	if(not quiet):
		root.mainloop()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	pigWins = 0
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
