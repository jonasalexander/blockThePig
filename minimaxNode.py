import random

class minimaxNode():

	def __init__(self, GS, parent):
		self.GS = GS

		# parent node
		self.parent = parent

		# child nodes
		self.children = []
		
		# index into children currently being explored
		self.exploredCounter = 0

		# value and pointer in minimax tree
		self.favoriteChildValue = None
		self.favoriteChild = None

		# simpleDepth includes player switches 
		# (so simpleDepth//numPlayers would be actual depth)
		if self.parent is None:
			self.simpleDepth = 0
		else:
			self.simpleDepth = self.parent.simpleDepth+1

	# Update children nodes with minimaxNodes from gameStates
	def addChildren(self, childrenGS):
		for state in childrenGS:
			self.children.append(minimaxNode(state, self))

	# essentially a .pop on the children that preserves the data
	def nextNode(self):
		if self.exploredCounter >= len(self.children):
			return None

		r = self.children[self.exploredCounter]
		self.exploredCounter += 1
		return r

	# Propagate children's heuristic values up the tree
	def findBestChild(self, compare):
		# if no children (for example because pig escaped/captured)
		if len(self.children) == 0:
			self.favoriteChild = None
			self.favoriteChildValue = 0
			return

		# allows flexibility to use same function for pig and stoneAgent
		if compare == 'min':
			def smaller(v1, v2): return v1 < v2
			compare = smaller
		elif compare == 'max':
			def larger(v1, v2): return v1 > v2
			compare = larger
		else:
			raise Exception("Received unexpeced type of comparison in findBestChild.")
		
		# find best value(s) among children
		best = self.children[0].favoriteChildValue
		fav = [self.children[0]]
		for child in self.children:
			if compare(child.favoriteChildValue, best):
				fav = [child]
				best = child.favoriteChildValue
			elif child.favoriteChildValue == best:
				fav.append(child)
		self.favoriteChildValue = best

		# if multiple favorite children, use tie breaker
		# intuition: works well if multiple placements along same corridor
		# towards exit possible (can just choose placement closest to pig)
		if len(fav) > 1:
			# tie breaker: distance of proposed stone placement to nearest pig
			bestDist = float("inf")
			tieBreaker = []
			for option in fav:
				newDist = option.GS.distanceToNearestPig(option.GS.lastMove)
				if compare(newDist, bestDist):
					bestDist = newDist
					tieBreaker = [option]
				elif newDist == bestDist:
					tieBreaker.append(option)
		else:
			self.favoriteChild = fav[0] # easy if one clearly favored child
			return

		# (if still multiple children, random tie breaker)
		# but will just select only value if now only 1 value
		self.favoriteChild = tieBreaker[random.randrange(len(tieBreaker))]

	def __str__(self):
		print 'Printing minimaxNode instance:'
		print 'self.GS.grid: ' + str(self.GS.grid)
		#print 'self.parent: ' + str(self.parent)
		print 'self.children: ' + str(self.children)
		print 'self.exploredCounter: ' + str(self.exploredCounter)
		print 'self.favoriteChildValue: ' + str(self.favoriteChildValue)
		return ''