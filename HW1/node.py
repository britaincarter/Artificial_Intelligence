class Node:

	def __key(self):
		string = '['.join('['.join('%s' %x for x in y) for y in self.state)
		hashcode = string.replace("[","")
		#print(hashcode)
		return hashcode
			
	'''def __eq__(x, y):
					return x.__key()==y.__key()
						
				def __hash__(self):
					return hash(self.__key())'''

	def __init__(self, state, parent, direction, depth, cost):
		self.state = state
		self.parent = parent
		self.depth = depth
		self.cost = cost
		self.direction = direction

	def __lt__(self, other):
		return self.cost <= other.cost

class Stack:
     def __init__(self):
         self.items = []

     # I have changed method name isEmpty to is_empty
     # because in your code you have used is_empty
     def is_empty(self):
         return self.items == []

     def contains(self, value):
     	for item in self.items:
     	 	if(value==item):
     	 		return True

     	return False


     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)