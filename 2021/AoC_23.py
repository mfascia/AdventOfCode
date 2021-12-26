import os
import sys
import queue
from copy import deepcopy


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = False
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------


DOORS = {
	"A": 2,
	"B": 4,
	"C": 6,
	"D": 8
}

VALID_CORRIDOR_POSITIONS = [0, 1, 3, 5, 7, 9, 10]

ENERGY_COSTS = {
	"A": 1,
	"B": 10,
	"C": 100,
	"D": 1000
}


def printStep(corridor, rooms):
	print("#############")
	print("#"+corridor+"#")
	print("#############")
	print(rooms)


def hash_state(state):
	s = state[0]
	for t, r in state[1].items():
		s += "".join(r)
	return hash(s) 


def main_1(inp):
	corridor = "..........."
	rooms = {
		"A": ["A", "B"],
		"B": ["D", "C"],
		"C": ["C", "B"],
		"D": ["A", "D"],
		# "A": ["C", "C"],
		# "B": ["A", "A"],
		# "C": ["D", "B"],
		# "D": ["B", "D"],
	}

	toVisit = queue.PriorityQueue()
	visited = {}

	toVisit.put((0, (corridor, rooms), None))

	while not toVisit.empty():
		print(toVisit.qsize())

		node = toVisit.get()
		currCost = node[0]
		currState = node[1]
		ch = hash_state(currState)
		currCorridor = currState[0]
		currRooms = currState[1]
		prev = node[2]

		visited[ch] = (currCost, currState, prev)

		for x in range(11):
			c = currCorridor[x]
			if c == ".":
				continue
			elif c in "ABCD":
				room = currRooms[c]
				if len(room) == 0 or all(map(lambda x: x==c.lower(), room)):
				# if len(room) == 0 or room[0] == c.lower():
					entrance = DOORS[c]
					clear = True
					if x < entrance:
						for i in range(x+1, entrance):
							if currCorridor[i] != ".":
								clear = False
								break
					else:
						for i in range(entrance, x):
							if currCorridor[i] != ".":
								clear = False
								break
					if clear:
						newCorridor = currCorridor[0:x] + "." + currCorridor[x+1:]
						newRooms = deepcopy(currRooms)
						newRooms[c].append(c.lower())
						newState = (newCorridor, newRooms)
						nh = hash_state(newState)
						newCost = currCost + (max(x, entrance) - min(x, entrance) + 1) * ENERGY_COSTS[c]
						if nh in visited:
							if visited[nh][0] > newCost:
								visited[nh][0] = newCost
								visited[nh][1] = newState
								visited[nh][2] = currState
						else:
							toVisit.put((newCost, newState, currState))

		for c, r in currRooms.items():
			if len(r) > 0 and r[-1].isupper():
				entrance = DOORS[c]
				for x in VALID_CORRIDOR_POSITIONS:
					clear = True
					for i in range(min(x, entrance), max(x,entrance)+1):
						if currCorridor[i] != ".":
							clear = False
							break
					if clear:
						newCorridor = currCorridor[0:x] + r[-1] + currCorridor[x+1:]
						newRooms = deepcopy(currRooms)
						newRooms[c].pop()
						newState = (newCorridor, newRooms)
						nh = hash_state(newState)
						newCost = currCost + (max(x, entrance) - min(x, entrance) + 1) * ENERGY_COSTS[c]
						if nh in visited: 
							if visited[nh][0] > newCost:
								visited[nh][0] = newCost
								visited[nh][1] = newState
								visited[nh][2] = currState
						else:
							toVisit.put((newCost, newState, currState))

	goal = ( "...........", {
		"A": ["a", "a"],
		"B": ["b", "b"],
		"C": ["c", "c"],
		"D": ["d", "d"],
	})

	node = goal
	path = []
	while node:
		path.append(node)
		node = visited[hash_state(node)][2]

	path = reversed(path)
	for p in path:
		printStep(p[0], p[1])

	print(visited[hash_state(goal)])



def main_2(inp):
	pass


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

if __name__ == "__main__":
	if doTests:
		# read tests
		if len(tests) == 0:
			i = 0
			while True:
				i += 1
				testfile = sys.argv[0].replace(".py", ("_test_%d.txt" % i))
				if os.path.isfile(testfile):
					tests.append([x for x in read_input(testfile)])
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = [x for x in read_input(sys.argv[0].replace(".py", "_input.txt"))]

	if doTests:
		# run tests
		isTest = True
		print ("--------------------------------------------------------------------------------")
		print ("- TESTS")
		print ("--------------------------------------------------------------------------------")
		for t in range(0, len(tests)):
			if enablePart1:
				print ("--- Test #" + str(t+1) + ".1 ------------------------------")
				main_1(tests[t])
			if enablePart2:
				print ("--- Test #" + str(t+1) + ".2 ------------------------------")
				main_2(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)