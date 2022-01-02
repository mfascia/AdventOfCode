import os
import sys
import queue
import heapq


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = [ "" ]
inp = "  "
isTest = False

doTests = False
doInput = True
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def djikstra(start, goal, nextFct):
	costs = {}
	predecessors = {}
	toVisit = queue.PriorityQueue()

	toVisit.put((0, start))
	predecessors[start] = None
	costs[start] = 0
	found = False

	while not toVisit.empty():
		print(toVisit.qsize())
		currentCost, currentNode = toVisit.get()
		if currentNode == goal:
			found = True
			break
		nextNodes, nextCosts = nextFct(currentNode)
		for i in range(len(nextNodes)):
			nextNode = nextNodes[i]
			nextCost = currentCost + nextCosts[i]
			
			if nextNode in costs and costs[nextNode] <= nextCost:
				continue
		
			costs[nextNode] = nextCost
			predecessors[nextNode] = currentNode
			toVisit.put((nextCost, nextNode))

	if found:
		path = []
		node = goal
		while node != None:
			path.append(node)
			node = predecessors[node]
		return reversed(path), costs[goal], predecessors, costs
	else:
		return [], -1, [], []


VALID_CORRIDOR_POSITIONS = [0, 1, 3, 5, 7, 9, 10]


def rooms_from_string(string, size):
	rooms = []
	for i in range(4):
		rooms.append(string[size*i:size*(i+1)].replace(".", ""))
	return rooms

def rooms_to_string(rooms, size):
	string = ""
	for i in range(4):
		string += rooms[i]
		for j in range(len(rooms[i]), size):
			string +="." 
	return string

def is_room_ready(room, letter):
	return all(map(lambda x: x==letter.lower(), room))


def is_path_clear(corridor, pod, entrance, includePod):
	if pod < entrance:
		start = pod if includePod else pod+1
		end = entrance
	else:
		start = entrance
		end = pod if includePod else pod-1
	
	clear  = True
	dist = 0
	for i in range(start, end+1):
		dist += 1
		if corridor[i] != ".":
			clear = False
			break

	return clear, dist


def nextStates(currState, roomSize):
	nextStates = []
	nextCosts = []

	currCorridor = currState[:11]
	currRoomsString = currState[11:]
	currRooms = rooms_from_string(currRoomsString, roomSize)

	for roomIndex in range(4):
		room = currRooms[roomIndex]
		if len(room) > 0 and room[-1].isupper():
			c = room[-1]
			entrance = (roomIndex)*2 + 2
			for x in VALID_CORRIDOR_POSITIONS:
				clear, dist = is_path_clear(currCorridor, x, entrance, True)
				if clear:
					newCorridor = currCorridor[0:x] + c + currCorridor[x+1:]
					newRooms = [cr for cr in currRooms]
					newRooms[roomIndex] = newRooms[roomIndex][:-1]
					newRoomsString = rooms_to_string(newRooms, roomSize)
					newState = newCorridor + newRoomsString
					nextStates.append(newState)
					dist += roomSize - len(room)
					nextCosts.append(dist * 10 ** "ABCD".index(c))

	for x in range(11):
		c = currCorridor[x]
		if c == ".":
			continue
		elif c in "ABCD":
			roomIndex = ord(c) - ord("A")
			room = currRooms[roomIndex]
			entrance = (roomIndex) * 2 + 2
			if is_room_ready(room, c):
				clear, dist = is_path_clear(currCorridor, x, entrance, False)
				if clear:
					newCorridor = currCorridor[0:x] + "." + currCorridor[x+1:]
					newRooms = [cr for cr in currRooms]
					newRooms[roomIndex] += c.lower()
					newRoomsString = rooms_to_string(newRooms, roomSize)
					newState = newCorridor + newRoomsString
					nextStates.append(newState)
					dist += roomSize - len(room)
					nextCosts.append(dist * 10 ** (roomIndex))

	return nextStates, nextCosts


def print_state(state, roomSize):
	print(".-----------.")
	print("|"+state[:11]+"|")
	for r in range(roomSize-1, -1, -1):
		print("'-|"+state[11+r]+"|"+state[11+roomSize+r]+"|"+state[11+2*roomSize+r]+"|"+state[11+3*roomSize+r]+"|-'")
	print("  '-------'")


def main(initial, goal, roomSize):
	roomsString = initial[11:]
	rooms = rooms_from_string(roomsString, roomSize)
	for r in range(4):
		tmp = ""
		canPin = True
		for i in range(len(rooms[r])):
			if canPin and rooms[r][i] == chr(ord("A")+r):
				tmp += rooms[r][i].lower()
			else:
				canPin = False
				tmp += rooms[r][i]
		rooms[r] = tmp

	initial = initial[:11] + rooms_to_string(rooms, roomSize)

	path, cost, preds, costs = djikstra(initial, goal, lambda x: nextStates(x, roomSize))
	for p in path:
		print_state(p, roomSize)
		print(costs[p])
	print(cost)


def main_1(inp):
	roomSize = 2
	if isTest:
		initial = "...........ABDCCBAD"
	else:
		initial = "...........CCAADBBD"
	goal = "...........aabbccdd"
	main(initial, goal, roomSize)


def main_2(inp):
	roomSize = 4
	if isTest:
		initial = "...........ADDBDBCCCABBACAD"
	else:
		initial = "...........CDDCABCADABBBCAD"
	goal = "...........aaaabbbbccccdddd"
	main(initial, goal, roomSize)


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