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


sim = Simulator("minimax", 10, 1, 1, 2, True)
sim.run()