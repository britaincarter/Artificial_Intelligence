import sys
import Queue as queue

#Check number of lines that match between the files
#For backTrack() all 400 matched, obtained all solutions.
#grep -F -f sudokus_finish.txt output_backtrack.txt | wc
#For obtaining non matching lines:
#grep -v -F -f sudokus_finish.txt output_backtrack.txt | wc

#For solveAC3() only 3 completed successfully

#Main driver
def run():
	if(len(sys.argv)!=2):
		print("Usage: python driver.py <input_string>")
		return
	elif(len(sys.argv[1])!=81):
		print("Your <input_string> is not the correct length")
		return
	line = sys.argv[1]
	#a = AC3_Sudoku(line)
	s = back_Sudoku(line)
	print("Initial : ")
	s.printGrid()
	s.backTrack()
	print("Finished : ")
	s.printGrid()
	s.writeOut()

#Class implementing CSP data structure with the algorithm AC3
#The initialization of the object is all you need to run and write the algorithm out to txt file
class AC3_Sudoku:

	board_dict = {}
	grid = []

	def __init__(self, line):
		self.board_dict = {}
		self.grid = [None]*81 
		self.load(line)
		self.create_dict()
		success = self.solveAC3()
		self.writeOut(success)

	def load(self, line):
		num = 0
		for c in line:
			if c == '\n' or c == '\r':
				break
			self.grid[num]= int(c)
			num+=1

	def create_dict(self):
		alph = ['A','B','C','D','E','F','G','H','I']
		num = 0
		for c in alph:
			for i in range(1, 10):
				s = c+str(i)
				self.board_dict[s]=self.grid[i-1 + num*9]
			num+=1	
		for k, v in self.board_dict.items():
			if v == 0:
				self.board_dict[k] = [1,2,3,4,5,6,7,8,9]
			else:
				self.board_dict[k] = [v]
	
	def writeOut(self, success):
		#Change to "a" for comparing both sudokus_finish.txt and output_ac3.txt
		#Uncomment below to compare the entire 400 lines. (run terminal commands as well)
		f = open("output_AC3.txt", "a")	
		if success == True:
			f.write("Success")
			'''
			alph = ['A', 'B', 'C', 'D','E','F','G','H','I']
			for c in alph:
				for i in range(1, 10):
					s = c+str(i)	
					sys.stdout.write(str(self.board_dict[s]))
			'''
		else:
			f.write("Unsuccessful")
		f.write("\n")
		f.close()	

	def printGrid(self):
		alph = ['A','B','C','D','E','F','G','H','I']
		num = 0
		for c in alph:
			for i in range(1, 10):
				s = c+str(i)
				sys.stdout.write(str(self.board_dict[s]))
			sys.stdout.write("\n")
				
	def cross(self, A, B):
		return [a+b for a in A for b in B]

	#Helper method for AC3
	def revise(self, x_i, x_j):
		#print()
		#print(self.board_dict)
		d_i = self.board_dict[x_i]
		d_j = self.board_dict[x_j]
		revised = False
		#print("x_i is ", x_i)
		#print("d_i is ", d_i)
		#print("x_j is ", x_j)
		#print("d_j is ", d_j)

		if len(d_i)==1:
			return False
		
		for d in d_i:
			if d in d_j and len(d_j)==1:
				d_i.remove(d)
				revised = True		
		self.board_dict[x_i] = d_i
		return revised
	
	def createQueue(self, squares, peers):
		q = []
		for s in squares:
			for p in peers[s]:
				q.append((s,p))

		return q

	def solveAC3(self):
		digits = '123456789'
		rows = 'ABCDEFGHI'
		cols = digits
		squares = self.cross(rows, cols)
		unitlist = ([self.cross(rows, c) for c in cols] +
			    [self.cross(r, cols) for r in rows] +
			    [self.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456', '789')])
		units = dict((s, [u for u in unitlist if s in u]) for s in squares)
		#print("UNITS: ",units)	
		peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)
		#print("\n")
		#print("SQUARES: ",squares)
		#print("\n")
		#print("PEERS: ", peers)		
		q = self.createQueue(squares, peers)
		while len(q)!=0:
			sq, peer = q.pop(0)
			#print("\n")
			#print("SQUARE: ",sq," PEER: ", peer)	
			if self.revise(sq, peer):
				if len(self.board_dict[sq])==0:
					print("Can't Solve")
					return False
				peers[sq].remove(peer)
				for k in peers[sq]:
					q.append((k, sq))
				
		v=1
		for k, v in self.board_dict.items():
			if len(v)!=1:
				#print("Did not solve.")
				v=0
				return False

		return True
	
#Back Tracking algorithm to solve all 400 given puzzles.
class back_Sudoku:

	grid = []

	def __init__(self, line):
		self.grid = []
		self.constructGrid(line)

	def writeOut(self):
		#Change to "a" for comparing both sudokus_finish.txt and output.txt
		#Uncomment below to compare the entire 400 lines. (run terminal commands as well)
		f = open("output.txt", "w")		
		for i in range(9):
			for j in range(9):
				f.write(str(self.grid[i][j]))

		f.write("\n")
		f.close()	

		
	def constructGrid(self, line):
		self.grid.append([])
		index = 0
		num=0
		for c in line:
			if(c=='\n' or c=='\r'):
				break
			if(num==8):
				num=0
				self.grid[index].append(int(c))
				index+=1
				self.grid.append([])
				continue
			num+=1
			self.grid[index].append(int(c))
		self.grid.pop()
		

	def findEmptyCell(self, x, y):
	    for i in range(x,9):
		    for j in range(y,9):
			    if self.grid[i][j] == 0:
				    return i,j
	    for i in range(0,9):
		    for j in range(0,9):
			    if self.grid[i][j] == 0:
				    return i,j
	    return -1,-1
	
	#Domains checkRow, checkColumn, checkBox	
	def checkRow(self, row, value):
	     for i in range(9):
			if self.grid[row][i] == value:
				return False

	     return True
	
	def checkColumn(self, column, value):
	     for i in range(9):
			if self.grid[i][column] == value:
				return False
	     return True

	def checkBox(self, row, column, value):
	     topR = 3*(row/3)
	     topC = 3*(column/3)	
	     for x in range(topR, topR+3):
		for y in range(topC, topC+3):
			if self.grid[x][y]==value:
				return False
	     return True

	def isLegal(self, value, x, y):
	     if self.checkRow(x, value):
		    if self.checkColumn(y, value):
	     		return self.checkBox(x, y, value)
	     return False

	
	def createQueue(self):
		q = []
		for i in self.domains:
			for j in self.arcs[i]:
				q.append(i, j)
		return q
	

	def backTrack(self, x=0, y=0):
		x, y = self.findEmptyCell(x, y)
		if x == -1 and y == -1:
		    return True
		value = 1
		while(value<10):
		    if self.isLegal(value, x, y): 
			    #Minimum remaining value heuristic 
			    self.grid[x][y] = value
			    if self.backTrack(x, y):
				    return True
			    #Undo for backtrack
			    self.grid[x][y] = 0
		    value+=1
		return False

	def printGrid(self):
		n=0
		b=0
		for x in range(0, 9):
			if n==3:
				print('-------------')
				n=0	
			n +=1
			for y in range(0,9):
				if(b%3==0):
					sys.stdout.write('|')
					b=0
				sys.stdout.write(str(self.grid[x][y]))		
				b+=1
			sys.stdout.write('|')
			sys.stdout.write('\n')	
		sys.stdout.write('\n\n')				




run()

#Testing with sudokus_start.txt and sudokus_finish.txt
'''
f = open("sudokus_start.txt")
games = []
i = 0
line = f.readline()
while line:
	games.append(line)
	line = f.readline()
	i+=1
f.close()
for g in games:
	s = AC3_Sudoku(g)
	
	
	#s = back_Sudoku(g)
	print("Initial: ")
	s.printGrid()
	s.backTrack() #Switch to s.solveAC3()
	print("Finished: ")
	s.printGrid()
	s.writeOut()
	

line2 = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
s2 = Sudoku(line2)
print("Hardest Sudoku")
print("Initial: ")
s2.printGrid()
s2.backTrack()
print("Finished: ")
s2.printGrid()
'''
	
