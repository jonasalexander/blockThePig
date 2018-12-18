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

def main(pigalgo, stonealgo, numStoneAgents, numPigAgents, maxDepth=None, quiet=False):


	if pigalgo == 'random':
		pigplayers =  [pigAgent.rrandomPigAgent(i) for i in range(numPigAgents)]
	elif pigalgo == 'simple':
		pigplayers =  [pigAgent.simplePigAgent(i) for i in range(numPigAgents)]
	elif pigalgo == 'complex':
		# TODO: there isnt really a pig complex agent... 
		pigplayers =  [pigAgent.simplePigAgent(i) for i in range(numPigAgents)]
	elif pigalgo == 'minimax':
		pigplayers =  [pigAgent.minimaxPigAgent(i) for i in range(numPigAgents)]
	elif pigalgo == 'alphabetaminimax':
		pigplayers =  [pigAgent.alphaBetaPigAgent(i) for i in range(numPigAgents)]
	else:
		raise Exception('Invalid algo name')


	if stonealgo == 'random':
		stoneplayers =  [stoneAgent.rrandomStoneAgent() for _ in range(numStoneAgents)]
	elif stonealgo == 'simple':
		stoneplayers =  [stoneAgent.simpleStoneAgent() for _ in range(numStoneAgents)]
	elif stonealgo == 'complex':
		stoneplayers =  [stoneAgent.complexStoneAgent() for _ in range(numStoneAgents)]
	elif stonealgo == 'minimax':
		stoneplayers =  [stoneAgent.minimaxStoneAgent() for _ in range(numStoneAgents)]
	elif stonealgo == 'alphabetaminimax':
		stoneplayers =  [stoneAgent.alphaBetaStoneAgent() for _ in range(numStoneAgents)]	
	else:
		raise Exception('Invalid algo name')

	players = pigplayers + stoneplayers
	
	GS = GameState(N_ROWS, N_COLS, players, numPigs=numPigAgents, quiet=quiet)
	
	# Tkinter window config
	if(not quiet):
		window = tk.Toplevel()
		window.title('Block The Pig')
		window.minsize(width=500, height=500)
		window.protocol('WM_DELETE_WINDOW', cleanUp)

	# Draw window
	if(not quiet):
		GS.draw(window)

	def update():
		if GS.allPigsEscaped() or GS.allPigsCaptured() or GS.allPigsEscapedOrCaptued():
			if(not quiet):
				cleanUp()
			# TODO: Count number of pigs escaped 
			
			score = GS.nPigsEscaped()
			print ('Game ended with:', score)
			return score

		GS.play() # where the magic happens
		if(not quiet):
			GS.draw(window)
			# Bug in line below
			root.after(TIME_DELAY, update)

		else:
			return(0 + update())

	if(not quiet):
		root.after(TIME_DELAY, update)
	else:
		return( 0 + update())

	#
	if(not quiet):
		root.mainloop()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	pigWins = 0
	# Optional Arguments
	parser.add_argument('-ns', help='Number of stone agents.', dest='numStoneAgents', default=1, type=int)
	parser.add_argument('-np', help='Number of pig agents.', dest='numPigAgents', default=1, type=int)
	
	parser.add_argument('-pa', help='Pig Agent', dest = 'pigAgent')
	parser.add_argument('-sa', help='Stone Agent', dest = 'stoneAgent')

	parser.add_argument('-d', help='If minimax game, the depth of the states the agents should explore.', dest='maxDepth',  default=None, type=int)
	parser.add_argument('-n', help='Number of games to simulare', dest='iterations', type = int, default = 1)


	args = parser.parse_args()

	for n in range(args.iterations):
		main(args.pigAgent, args.stoneAgent, args.numStoneAgents, args.numPigAgents)
