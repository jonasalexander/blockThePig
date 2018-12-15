from util import *
from main import *

class Simulator():
    def __init__(self, gameType, number, nStoneAgents, nPigAgents, maxDepth, quiet):
        self.gameType = gameType
        self.quiet = quiet
        self.num = number
        self.nStoneAgents = nStoneAgents
        self.nPigAgents = nPigAgents
        self.maxDepth = maxDepth

        self.pigWins = 0
    
    def run(self):
        for n in range(self.num):
            b = main(self.gameType, self.nStoneAgents, self.nPigAgents, self.maxDepth, self.quiet)
            if b:
                self.pigWins +=1
        print ('pig win rate:', float(self.pigWins)/float(self.num))
        return

parser = argparse.ArgumentParser()
pigWins = 0
# Optional Arguments
parser.add_argument('-ns', help='Number of stone agents.', dest='numStoneAgents', default=1, type=int)
parser.add_argument('-np', help='Number of pig agents.', dest='numPigAgents', default=1, type=int)

parser.add_argument('-g', help='Game type.', dest='gameType', type = str, default = "simple")
parser.add_argument('-d', help='If minimax game, the depth of the states the agents should explore.', dest='maxDepth',  default=None, type=int)
parser.add_argument('-n', help='Number of games to simulare', dest='iterations', type = int, default = 1)
parser.add_argument('-q', help='Whether to show graphics', dest='quiet', action = 'store_true')

args = parser.parse_args()
print "self.quiet", args.quiet
sim = Simulator(args.gameType, args.iterations, args.numStoneAgents, args.numPigAgents, args.maxDepth, args.quiet)
sim.run()