from util import *
from main import *
num = 10
nStoneAgents = 1
nPigAgents = 1
maxDepth = 2

for n in range(num):
    main('minimax', nStoneAgents, nPigAgents, maxDepth)
    print ("pig wins at", n, ":", pigWins)
print ('pig win rate:', pigWins/num)
