import sys
import time
import psutil
import os
#import resource

#from memory_profiler import memory_usage
#cmdargs = str(sys.argv)

'''def memory():
    import os
    from wmi import WMI
    w = WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)

'''

start = time.time()

#print ("The total numbers of args passed to the script: %d " % total)
#print ("Args list: %s " % cmdargs)
#print ("Script name: %s" % str(sys.argv[1]))
#print("Board sequence: %s"% str(sys.argv[2]))

from searchAlgorithms import bfs
process = psutil.Process(os.getpid())
_1stmemory = process.memory_info().rss
goal = bfs("3,1,2,0,4,5,6,7,8")
max_fringe_size = goal[1]
fringe_size = goal[2]
_2ndmemory = process.memory_info().rss

memory = _2ndmemory-_1stmemory 



#memory = process.

from state import numberOfNodes
from state import nodes_expanded

#memory = memory_usage((bfs, "1,2,5,3,4,0,6,7,8"))
#memory = memory()
#memory = process.get_memory_info()[0]/float(2**20)

end = time.time()

#max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000

#print (goal.state)

path_to_goal = []
node = goal[0]
while node.parent != None:
	path_to_goal.insert(0, node.direction)
	node = node.parent


print("path_to_goal: ", path_to_goal)
print("cost_of_path: ", goal[0].depth)
print("nodes_expanded: ", len(nodes_expanded))
print("fringe_size: ", fringe_size)
print("max_fringe_size: ", max_fringe_size)
print("search_depth: ", goal[0].depth)
print("running_time: ", end - start)
print("max_ram_usage: ", memory)

'''
if(total!= 3):
	sys.exit()

if(sys.argv[1]=="bfs"):
	from searchAlgorithms import bfs
	list = bfs(sys.argv[2])
elif(sys.argv[1]=="dfs"):
	from searchAlgorithms import dfs
	list = dfs(sys.argv[2])
elif(sys.argv[1]=="ast"):
	from searchAlgorithms import ast
	list = ast(sys.argv[2])
elif(sys.argv[1]=="ida"):
	from searchAlgorithms import ida
	list = ida(sys.argv[2])


print (list)
'''