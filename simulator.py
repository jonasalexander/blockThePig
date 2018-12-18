from util import *
from main import *

class Simulator():
    def __init__(self, pigAlgo, stoneAlgo,  number, nStoneAgents, nPigAgents, maxDepth, quiet):
        # self.gameType = gameType
        self.quiet = quiet
        self.num = number
        self.nStoneAgents = nStoneAgents
        self.nPigAgents = nPigAgents
        self.maxDepth = maxDepth
        self.pigAlgo = pigAlgo
        self.stoneAlgo = stoneAlgo

        self.pigWins = 0

    def run(self):
        for n in range(self.num):
            b = main(self.pigAlgo, self.stoneAlgo, self.nStoneAgents, self.nPigAgents, self.maxDepth, self.quiet)
            #the following line is a bug when you are not in quiet mode - bug source can be found in line 62? it says bug below in line 61
            self.pigWins +=  b
        print ('pig win rate:', float(self.pigWins)/float(self.num))
        return

parser = argparse.ArgumentParser()
pigWins = 0
# Optional Arguments
parser.add_argument('-ns', help='Number of stone agents.', dest='numStoneAgents', default=1, type=int)
parser.add_argument('-np', help='Number of pig agents.', dest='numPigAgents', default=1, type=int)

parser.add_argument('-pa', help='Pig Agent', dest = 'pigAgent')
parser.add_argument('-sa', help='Stone Agent', dest = 'stoneAgent')

parser.add_argument('-g', help='Game type.', dest='gameType', type = str, default = "simple")
parser.add_argument('-d', help='If minimax game, the depth of the states the agents should explore.', dest='maxDepth',  default=None, type=int)
parser.add_argument('-n', help='Number of games to simulare', dest='iterations', type = int, default = 1)

#this following line doenst do what i expect it to do. if you dont add anthing self.quit is False as per
# default if you have eitherl -q True or -q False you get self.quite is True just fyi
parser.add_argument('-q', help='Whether to show graphics', dest='quiet', default = False, type  = bool )

args = parser.parse_args()
# print ("self.quiet", args.quiet)
sim = Simulator(args.pigAgent, args.stoneAgent,  args.iterations, args.numStoneAgents, args.numPigAgents, args.maxDepth, args.quiet)
sim.run()