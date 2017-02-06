from numpy import *
from state import *
from node import *
from queue import *
from heapq import *
from collections import deque
import heapq

def bfs(Board):
	b = initialize(Board)
	neighborsList = []
	frontier = deque()
	frontier.append(create_node(b, None, None, 0, 0 ))
	length = 0
	explored = set()

	while frontier:
		node = frontier.popleft()
		
		string = '['.join('['.join('%s' %x for x in y) for y in node.state)
		hashcode = string.replace("[","")
		#print(hashcode in explored)
		if(hashcode in explored):
			#print("rejected: ", node.state)
			continue
		#print("Added to explored: ", node.state)			
		explored.add(hashcode)
		#print(explored)
		if(goalTest(node)):
			lst = []
			lst.append(node)
			lst.append(length)
			lst.append(len(frontier))
			return lst

		neighborsList = neighbors(node)
		#print(neighborsList)
		for neighbor in neighborsList:
			string = '['.join('['.join('%s' %x for x in y) for y in neighbor.state)
			hashcode = string.replace("[","")
			if(hashcode in explored):
				#print("rejected: ", node.state)
				continue
			elif(neighbor not in frontier):
				#print("Added to frontier: ",neighbor.state)
				frontier.append(neighbor)
				length += 1
			
	return False				

#print(node.state)
'''
string = '['.join('['.join('%s' %x for x in y) for y in node.state)
hashlist = string.replace("[","")
'''


def dfs(Board):
	b = initialize(Board)
	neighborsList = []
	frontier = set()
	explored = set()

	frontier.add(create_node(b, None, None, 0, 0 ))
	length = 1

	while frontier:

		node = frontier.pop()
		
		string = '['.join('['.join('%s' %x for x in y) for y in node.state)
		hashcode = string.replace("[","")

		if(hashcode in explored):
			continue

		print("Added to explored: ", node.state)			
		explored.add(hashcode)

		print(explored)

		if(goalTest(node)):
			lst = []
			lst.append(node)
			#length = len(frontier)
			#print(length)
			lst.append(length)
			return lst

		neighborsList = neighbors(node)
		for neighbor in neighborsList:
			string = '['.join('['.join('%s' %x for x in y) for y in neighbor.state)
			hashcode = string.replace("[","")
			if(hashcode in explored):
				continue
			elif(neighbor not in frontier):
				frontier.add(neighbor)
				length += 1
			
	return False		

def ast(Board):
	b = initialize(Board)
	neighborsList = []
	frontier = []
	cost = manhattanCostFunction(b)
	heappush(frontier, create_node(b, None, None, 0, cost ))
	explored = set()

	while frontier:
		node = heappop(frontier)
		string = '['.join('['.join('%s' %x for x in y) for y in node.state)
		hashcode = string.replace("[","")
		#print(hashcode in explored)
		if(hashcode in explored):
			#print("rejected: ", node.state)
			continue
		#print("Added to explored: ", node.state)			
		explored.add(hashcode)
		#print(explored)
		if(goalTest(node)):
			lst = []
			lst.append(node)
			length = len(frontier)
			print(length)
			lst.append(length)
			return lst

		neighborsList = neighbors_ast(node)
		#print(neighborsList)
		for neighbor in neighborsList:
			string = '['.join('['.join('%s' %x for x in y) for y in neighbor.state)
			hashcode = string.replace("[","")
			if(hashcode in explored):
				#print("rejected: ", node.state)
				continue
			elif(neighbor not in frontier):
				#print("Added to frontier: ",neighbor.state)
				heappush(frontier, neighbor)
			
	return False	



def ida(Board):
	print(Board + " IDA")
	return
