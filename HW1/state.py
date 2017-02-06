from node import *
from copy import deepcopy
import math

def square_root(length):
	size = length+1
	size = size ** .5
	N = int(size)
	return N

def goalTest(node):
	#print(goalBoardTest)
	#print(node.depth, node.state, node.direction)
	if(node.state == goalBoardTest):
		return True

	return False

def findEmptySpace(board):
	#print(len(board))
	for i in range(len(board)):
		for j in range(len(board)):
			if(board[i][j]==0):
				#print (i, j)
				position = []
				position.append(i)
				position.append(j)				
				return position

def addNode():
	numberOfNodes[0] += 1

def create_node(state, parent, direction, depth, cost):
	addNode()
	return Node(state, parent, direction, depth, cost)

class state(object):

	board = None

	def __hash__(self):
		return hash((self.__class__))

	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return NotImplemented
		return self.board == other.board


	def instantiate(size):
		board = [[0 for size in range(size)] for y in range(size)]
		return board
		

def checkIfLegalDirection(state, emptySpace, direction):
	
	xloc = emptySpace[0]
	yloc = emptySpace[1]


	if(direction == "Up" and xloc-1 >= 0):
		return True
	elif(direction == "Down" and xloc+1<N):
		return True
	elif(direction == "Left" and yloc-1>=0):
		return True
	elif(direction == "Right" and yloc+1<N):
		return True
	return False

#Implemented algorithm from stack
#http://stackoverflow.com/questions/12526792/manhattan-distance-in-a
def manhattanCostFunction(state):
	cost = 0
	manhattanDistanceSum = 0
	row = 0
	column = 0

	while row<N:
		column = 0
		while column < N:
			value = state[row][column]; # tiles array contains board elements
			if (value != 0): # we don't compute MD for element 0
				targetRow = (value - 1) / N; # expected x-coordinate (row)
				targetColumn = (value - 1) % N; # expected y-coordinate (col)
				dx = row - targetRow; # x-distance to expected coordinate
				dy = column - targetColumn; # y-distance to expected coordinate
				manhattanDistanceSum += math.fabs(dx) + math.fabs(dy); 
			column+=1
		row+=1
	cost = manhattanDistanceSum
	return cost

def neighbors_ast(node):
	neighbors = []
	emptySpace = findEmptySpace(node.state)
	nodes_expanded.append(node)

	if(checkIfLegalDirection(node.state, emptySpace, "Up")):
		newState = move_up(node.state, emptySpace)
		cost = manhattanCostFunction(newState)
		newNode = create_node(newState, node, "Up", node.depth+1, cost)
		neighbors.append(newNode)
	
	if(checkIfLegalDirection(node.state, emptySpace, "Down")):
		newState = move_down(node.state, emptySpace)
		cost = manhattanCostFunction(newState)
		newNode = create_node(newState, node, "Down", node.depth+1, cost)
		neighbors.append(newNode)
	
	if(checkIfLegalDirection(node.state, emptySpace, "Left")):
		newState = move_left(node.state, emptySpace)
		cost = manhattanCostFunction(newState)
		newNode = create_node(newState,  node, "Left", node.depth+1,cost)
		neighbors.append(newNode)
	
	if(checkIfLegalDirection(node.state, emptySpace, "Right")):
		newState = move_right(node.state, emptySpace)
		cost = manhattanCostFunction(newState)
		newNode = create_node(newState, node, "Right", node.depth+1,cost)
		neighbors.append(newNode)	
	
	print()
	print("Parent: ", node.state, node.cost)
	for item in neighbors:
		print(item.state, item.direction, item.cost)


	return neighbors

def neighbors_dfs(node):
	neighbors = []

	emptySpace = findEmptySpace(node.state)

	
	nodes_expanded.append(node)

	if(checkIfLegalDirection(node.state, emptySpace, "Right")):
		newState = move_right(node.state, emptySpace)
		newNode = create_node(newState, node, "Right", node.depth+1,0)
		neighbors.append(newNode)	
	if(checkIfLegalDirection(node.state, emptySpace, "Left")):
		newState = move_left(node.state, emptySpace)	
		newNode = create_node(newState,  node, "Left", node.depth+1,0)
		neighbors.append(newNode)
	if(checkIfLegalDirection(node.state, emptySpace, "Down")):
		newState = move_down(node.state, emptySpace)	
		newNode = create_node(newState, node, "Down", node.depth+1,0)
		neighbors.append(newNode)
	if(checkIfLegalDirection(node.state, emptySpace, "Up")):
		newState = move_up(node.state, emptySpace)	
		newNode = create_node(newState, node, "Up", node.depth+1,0)
		neighbors.append(newNode)
	print()
	print("Parent: ", node.state)
	for item in neighbors:
		print(item.state, item.direction)


	return neighbors


def neighbors(node):
	'''
	DOWN = [1, 0]
	UP = [-1, 0]
	LEFT = [0, -1]
	RIGHT = [0, 1]
	'''
	neighbors = []

	emptySpace = findEmptySpace(node.state)

	
	nodes_expanded.append(node)

	if(checkIfLegalDirection(node.state, emptySpace, "Up")):
		newState = move_up(node.state, emptySpace)	
		newNode = create_node(newState, node, "Up", node.depth+1,0)
		neighbors.append(newNode)
	if(checkIfLegalDirection(node.state, emptySpace, "Down")):
		newState = move_down(node.state, emptySpace)	
		newNode = create_node(newState, node, "Down", node.depth+1,0)
		neighbors.append(newNode)
	if(checkIfLegalDirection(node.state, emptySpace, "Left")):
		newState = move_left(node.state, emptySpace)	
		newNode = create_node(newState,  node, "Left", node.depth+1,0)
		neighbors.append(newNode)
	if(checkIfLegalDirection(node.state, emptySpace, "Right")):
		newState = move_right(node.state, emptySpace)
		newNode = create_node(newState, node, "Right", node.depth+1,0)
		neighbors.append(newNode)	
	
	print()
	print("Parent: ", node.state)
	for item in neighbors:
		print(item.state, item.direction)


	return neighbors
	

def move_up(state, emptySpace):

	xloc = emptySpace[0]
	yloc = emptySpace[1]

	changed_state = deepcopy(state)
	
	temp = changed_state[xloc-1][yloc]
	changed_state[xloc-1][yloc]=changed_state[xloc][yloc]
	changed_state[xloc][yloc]=temp

	return changed_state

def move_down(state, emptySpace):

	xloc = emptySpace[0]
	yloc = emptySpace[1]

	changed_state = deepcopy(state)

	temp = changed_state[xloc+1][yloc]
	changed_state[xloc+1][yloc]=changed_state[xloc][yloc]
	changed_state[xloc][yloc]=temp

	return changed_state

def move_left(state, emptySpace):	
	xloc = emptySpace[0]
	yloc = emptySpace[1]

	changed_state = deepcopy(state)
	
	temp = changed_state[xloc][yloc-1]
	changed_state[xloc][yloc-1]=changed_state[xloc][yloc]
	changed_state[xloc][yloc]=temp

	return changed_state

def move_right(state, emptySpace):	

	xloc = emptySpace[0]
	yloc = emptySpace[1]

	changed_state = deepcopy(state)
	
	temp = changed_state[xloc][yloc+1]
	changed_state[xloc][yloc+1]=changed_state[xloc][yloc]
	changed_state[xloc][yloc]=temp

	return changed_state

def initialize(argv1):
	list = argv1.split(',')
	length = len(list)
	
	#length of row/columns
	global goalBoardTest 
	global N
	global numberOfNodes
	global nodes_expanded
	nodes_expanded = []
	numberOfNodes=[]
	numberOfNodes.append(0)
	N = square_root(length)

	goalBoardTest = [[0 for size in range(N)] for y in range(N)]

	row = 0
	column = 0
	indx = 0

	board = [[0 for N in range(N)] for y in range(N)]
	

	while row<N:
		column = 0
		while column < N:
			item = list[indx]
			number = int(item)
			board[row][column] = number
			goalBoardTest[row][column] = indx
			column+=1
			indx += 1
		row+=1
	goalBoardTest[row-1][column-1]=indx-1
	goalBoardTest[0][0]=0
	#print(goalBoardTest)
	return board