import os
import sys
import queue
import heapq


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = [ "" ]
inp = ""
isTest = False

doTests = True
doInput = False
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------



VALID_CORRIDOR_POSITIONS = [0, 1, 3, 5, 7, 9, 10]
ROOM_SIZE = 2


def rooms_from_string(string, size=ROOM_SIZE):
	rooms = []
	for i in range(4):
		rooms.append(string[size*i:size*(i+1)].replace(".", ""))
	return rooms

def rooms_to_string(rooms, size=ROOM_SIZE):
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
	for i in range(start, end):
		dist += 1
		if corridor[i] != ".":
			clear = False
			break

	return clear, dist


def main_1(inp):
	initialState = "...........ABDCCBAD"

	# toVisit = queue.PriorityQueue()
	toVisit = []
	visited = {}

	# toVisit.put((0, initialState, None))
	heapq.heappush( toVisit, (0, initialState, None))

	costs = {}

	while len(toVisit) > 0:


		node = heapq.heappop(toVisit)
		print(len(toVisit), node)

		currCost = node[0]

		currState = node[1]

		prev = node[2]

		currCorridor = currState[:11]
		currRoomsString = currState[11:]
		currRooms = rooms_from_string(currRoomsString)

		for roomIndex in range(4):
			room = currRooms[roomIndex]
			if len(room) > 0 and room[-1].isupper():
				c = room[-1]
				entrance = (roomIndex)*2 + 2
				for x in VALID_CORRIDOR_POSITIONS:
					clear, dist = is_path_clear(currCorridor, x, entrance, True)
					if clear:
						dist += ROOM_SIZE - len(room)
						newCorridor = currCorridor[0:x] + c + currCorridor[x+1:]
						newRooms = [cr for cr in currRooms]
						newRooms[roomIndex] = newRooms[roomIndex][:-1]
						newRoomsString = rooms_to_string(newRooms)
						newState = newCorridor + newRoomsString
						newCost = currCost + dist * 10 ** (roomIndex)
						if not newState in visited or visited[newState][0] > newCost:
							newTuple = (newCost, newState, currState)
							visited[newState] = newTuple
							heapq.heappush(toVisit, newTuple)
					else:
						break


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
						dist += ROOM_SIZE - len(room)
						newCorridor = currCorridor[0:x] + "." + currCorridor[x+1:]
						newRooms = [cr for cr in currRooms]
						newRooms[roomIndex] += c.lower()
						newRoomsString = rooms_to_string(newRooms)
						if newRoomsString == "aabbccdd":
							print("reached the goal!!!!")
						newState = newCorridor + newRoomsString
						newCost = currCost + dist * 10 ** (roomIndex)
						if not newState in visited or visited[newState][0] > newCost:
							newTuple = (newCost, newState, currState)
							visited[newState] = newTuple
							heapq.heappush(toVisit, newTuple)



	goal = "...........aabbccdd"

	node = goal
	path = []
	while node:
		print(visited[node][0], node[:11], node[11:])
		path.append(node)
		node = visited[node][2]

	path = reversed(path)
	for p in path:
		print(p[:11], p[11:])

	print(visited[goal])



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