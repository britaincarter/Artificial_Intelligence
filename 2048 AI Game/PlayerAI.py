'''
Up - 0
Down - 1
Left - 2
Right - 3
'''

from random import randint
from BaseAI import BaseAI
from Grid import Grid
import math
import time
 
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

def findFarthestPosition(grid, x, y, vector):
	previous = None
	while(cellAvailable(grid, x, y)):
		previous = grid.map[x][y]
		x += vector[0]
		y += vector[1]
	alist = []
	x-=vector[0]
	y-=vector[1]
	alist.append(x)
	alist.append(y)	
	return alist

def cellAvailable(grid, x, y):
	if(x<0 or x>3 or y<0 or y>3):
		return False
	if(grid.map[x][y]!=0):
		return True 
	return False


def printGrid(grid):
	string =[] 
	for x in xrange(grid.size):
		for y in xrange(grid.size):
			string.append(grid.map[x][y])
	
	print(string)
	return

def maxedge(grid):
	value = 0
	firstRow     = grid.map[0][0] + grid.map[0][1] + grid.map[0][2] + grid.map[0][3]
	secondRow    = grid.map[3][0] + grid.map[3][1] + grid.map[3][2] + grid.map[3][3]
	firstColumn  = grid.map[0][0] + grid.map[1][0] + grid.map[2][0] + grid.map[3][0]
	secondColumn = grid.map[0][3] + grid.map[1][3] + grid.map[2][3] + grid.map[3][3]
	best = max(firstRow, secondRow, firstColumn, secondColumn)
	if best==0:
		return 0
	else: 
		value = math.log(best)/math.log(2)
		return value


def weightedCorner(grid):
	r1 = 4 * grid.map[0][0] + 2*(grid.map[0][1]+grid.map[1][0])+(grid.map[0][2]+grid.map[1][1]+grid.map[2][0])
	r2 = 4 * grid.map[3][3] + 2*(grid.map[3][2]+grid.map[2][3])+(grid.map[3][1]+grid.map[2][2]+grid.map[1][3])
	best = max(r1, r2)
	return best

'''
def maxCorner(grid):
	r1 = weightedCorner(grid)

	r2 = weigtedCorner(rotate)
	best = max(r1, r2)
	value = math.log(best)/math.log(2)
	return value
'''

#Implemented code that was in the discussion on stack overflow for the heuristic
#Specifically monotoniciy, smoothness, empty cells, and largest value tile
def heuristic(grid): #expandedNodes):
	value = 0
	value += smoothness(grid) * smoothWeight
	value += monotonicity(grid) * monoWeight 
	value += math.log(grid.getMaxTile()) * maxWeight# **2/4
	value += len(grid.getAvailableCells())/math.log(2)*emptyWeight
	value += maxedge(grid) * edgeWeight
	#value += maxCorner(grid)*maxCornerWeight
	#alist = []
	#alist.append(value)
	#alist.append(expandedNodes)
	#return alist
	return value

def smoothness(grid):
	smoothness = 0
	direction = None
	xAxis = 0
	yAxis = 0
	previous = None
	for x in xrange(grid.size):
		for y in xrange(grid.size):	
			if(grid.map[x][y] != 0):
				value = math.log(grid.map[x][y])/math.log(2)
				for d in xrange(1, 2):
					vector = directionVectors[d]
					alist = []
					alist = findFarthestPosition(grid, x, y, vector)
					xAxis = alist[0]
					yAxis = alist[1]
					targetCell = grid.map[xAxis][yAxis]
					if(targetCell!=0):
						targetValue = math.log(targetCell)/math.log(2)
						smoothness -= abs(value - targetValue)
	return smoothness
		

def monotonicity(grid):
	value = 0
	totalsX = [0, 0]
	totalsY = [0, 0]
	for x in xrange(grid.size):
		current = 0
		nextOne = current + 1
		while(nextOne < 4):
			while(nextOne<4 and grid.map[x][nextOne]==0):
				nextOne += 1
			if(nextOne>=4):
				nextOne -= 1
			
			if(grid.map[x][current]!=0):
				currentValue = math.log(grid.map[x][current])/math.log(2)
			else:
				currentValue = 0

			if(grid.map[x][nextOne]):
				nextValue = math.log(grid.map[x][nextOne])/math.log(2)
			else:
				nextValue = 0
			if(currentValue > nextValue):
				totalsX[0] += nextValue - currentValue
			elif(nextValue > currentValue):
				totalsX[1] += currentValue - nextValue
			current = nextOne
			nextOne += 1

	for y in xrange(grid.size):
		current = 0
		nextOne = current + 1
		while(nextOne < 4):
			while(nextOne<4 and grid.map[nextOne][y]==0):
				nextOne += 1
			if(nextOne>=4):
				nextOne -= 1
			if(grid.map[current][y]!=0):
				currentValue = math.log(grid.map[current][y])/math.log(2)
			else:
				currentValue = 0
			if(grid.map[nextOne][y]):
				nextValue = math.log(grid.map[nextOne][y])/math.log(2)
			else:
				nextValue = 0
			if(currentValue > nextValue):
				totalsY[0] += nextValue - currentValue
			elif(nextValue > currentValue):
				totalsY[1] += currentValue - nextValue
			current = nextOne
			nextOne += 1

	value = max(totalsX) + max(totalsY)
	return value


def minimax(grid, depth, player):
	global timer
	if time.clock() - timer > .0001 or len(grid.getAvailbleMoves())==0:
		return heuristic(grid)	
	if(depth == 0):
		return heuristic(grid)

	if(player):#Maximize
		maxUtility = -999999
		for direction in grid.getAvailableMoves():
			gridCopy = grid.clone()
			gridCopy.move(direction)
			utility = minimax(gridCopy, depth, 0)
			if(utility > maxUtility):
				maxUtility = utility
		return maxUtility
	else:#Minimize
		minUtility = 999999
		for cell in grid.getAvailableCells():
			gridCopy = grid.clone()
			gridCopy.insertTile(cell, 2)
			utility = minimax(gridCopy, depth-1, 1)
			if(utility < minUtility):
				minUtility = utility
		return minUtility

def alphaBeta(grid, alpha, beta, depth, player):   #, expandedNodes):
	global timer
	if time.clock() - timer > .000001 or len(grid.getAvailbleMoves())==0:
		#expandedNodes += 1
		return heuristic(grid) #,expandedNodes)	
	if(depth == 0):
		#expandedNodes += 1
		return heuristic(grid) #,expandedNodes)
	utility = 0
	if(player):#Maximize
		maxUtility = -999999
		for direction in grid.getAvailableMoves():
			gridCopy = grid.clone()
			gridCopy.move(direction)
			#alist = []
			utility = alphaBeta(gridCopy, alpha, beta, depth-1, 0 )  #, expandedNodes)
			#utility = alist[0]
			#expandedNodes += alist[1]	
			if(utility > maxUtility):	
				maxUtility = utility
			if(maxUtility >= beta):
				break
			if(maxUtility > alpha):
				alpha = maxUtility	
		#secondlist = []
		#secondlist.append(maxUtility)
		#secondlist.append(expandedNodes)
		#return secondlist
		return maxUtility
	else:#Minimize
		minUtility = 999999
		for cell in grid.getAvailableCells():
			gridCopy = grid.clone()
			gridCopy.insertTile(cell, 2)
			#alist = []
			utility = alphaBeta(gridCopy, alpha, beta, depth-1, 1)    #, expandedNodes)
			#utility = alist[0]
			#expandedNodes += alist[1]
			if(utility < minUtility):
				minUtility = utility		
			if(minUtility <= alpha):
				break
			if(minUtility < beta):
				beta = minUtility
		#secondlist = []
		#secondlist.append(minUtility)
		#secondlist.append(expandedNodes)	
		#return secondlist 
		return minUtility




#Change either to alphaBeta or miniMax below
class PlayerAI(BaseAI):
	
	global smoothWeight, monoWeight, emptyWeight, maxWeight, lengthTree, timer, edgeWeight, maxCornerWeight
	maxCornerWeight = 1.0
	smoothWeight = .1
	monoWeight = 1.0 
	emptyWeight = 2.7 
	maxWeight = 1.0
	lengthTree = 5
	timer = 0
	edgeWeight = .8

	def getMove(self, grid):
		timer = time.clock() 
		bestMove = 0
		maxUtility = 0
		bestMove = 0
		utility = 0	
		#returnNodes = []
		#expandedNodes = 0
		#Minimax
		'''
		for direction in grid.getAvailableMoves():
			newGrid = grid.clone()
			newGrid.move(direction)
			utility = minimax(newGrid, lengthTree,1)
			if(utility > maxUtility):
				maxUtility = utility
				bestMove = direction
		'''
		#Alpha-Beta	
		downMove = 0
		for direction in grid.getAvailableMoves():
			newGrid = grid.clone()
			newGrid.move(direction)
			utility = alphaBeta(newGrid, -999999, 999999, lengthTree, 1)  #, expandedNodes)
			#utility = returnNodes[0]
			#expandedNodes += returnNodes[1]
			if(direction == 1):
				downMove = utility
			if(utility > maxUtility):
				maxUtility = utility
				bestMove = direction

		#print("Nodes : ",expandedNodes)
		return bestMove


		
