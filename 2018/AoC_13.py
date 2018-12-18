import os
import sys
from PIL import Image


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------
turns = {
	"^": {
		0: "<",	
		1: "^",	
		2: ">",	
		},
	"<": {
		0: "v",	
		1: "<",	
		2: "^",	
		},
	"v": {
		0: ">",	
		1: "v",	
		2: "<",	
		},
	">": {
		0: "^",	
		1: ">",	
		2: "v",	
		},
	}
dirs = {
	"^": [0, -1],
	"<": [-1, 0],
	"v": [0, 1],
	">": [1, 0],
}
trackTurn = {
	"/": {
		"^": ">",
		"<": "v",
		"v": "<",
		">": "^"
	},
	"\\": {
		"^": "<",
		"<": "^",
		"v": ">",
		">": "v"
	}
}


def move(tracks, train):
	dir = train[1]
	train[0] = map(lambda x: sum(x), zip(train[0], dirs[dir]))
	track = tracks[train[0][1]][train[0][0]]
	if track == "+":
		train[1] = turns[train[1]][train[2]%3]
		train[2] += 1
	elif track == "/" or track == "\\":
		train[1] = trackTurn[track][train[1]]
	return train


def read_tracks(inp):
	tracks = []
	trains = []
	y = 0
	for line in inp:
		edited = ""
		for i in xrange(0, len(line)):
			if line[i] in "<>^v":
				trains.append([[i, y], line[i], 0])
				edited += "|" if line[i] in "v^" else "-"
			else:
				edited += line[i]
		tracks.append(edited)
		y += 1
	return tracks, trains


def print_state(time, tracks, trains):
	print "t=" + str(time)
	for y in xrange(0, len(tracks)):
		line = format(y, "3d") + ": "
		for x in xrange(0, len(tracks[0])):
			c = tracks[y][x]
			for t in trains:
				if t[0][0] == x and t[0][1] == y:
					c = t[1]
					break
			line += c
		print line
	for t in trains:
		print t


def save_state(time, tracks, trains):
	im = Image.new(mode="RGB", size=(len(tracks[0]), len(tracks)))	
	for y in xrange(0, len(tracks)):
		for x in xrange(0, len(tracks[0])):
			c = (127, 127, 127) if tracks[y][x] != " " else (0, 0, 0)
			for t in trains:
				if t[0][0] == x and t[0][1] == y:
					c = (255, 0, 0)
					break
			im.putpixel((x, y), c)

	im.save(sys.argv[0].replace(".py", "_" + format(time, "03d") + ".png"))


def main_1(inp):
	tracks, trains = read_tracks(inp)
	t = 0
	while True:
		#save_state(t, tracks, trains)
		t += 1
		trains.sort(key=lambda x: (x[0][1], x[0][0]))
		for train in trains:
			train = move(tracks, train)

		for t1 in xrange(0, len(trains)-1):
			for t2 in xrange(t1+1, len(trains)):
				if trains[t1][0][0] == trains[t2][0][0] and trains[t1][0][1] == trains[t2][0][1]:
					print "Collision at t=", t, "and location=", trains[t1][0], "between trains", t1, "and", t2
					#save_state(t, tracks, trains)
					return


def main_2(inp):
	tracks, trains = read_tracks(inp)
	t = 0
	while 100000:
		t += 1
		trains.sort(key=lambda x: (x[0][1], x[0][0]))
		collided = []
		for t1 in xrange(0, len(trains)):
			if not trains[t1]:
				continue
			trains[t1] = move(tracks, trains[t1])
			for t2 in xrange(0, len(trains)):
				if not trains[t2] or t1==t2:
					continue
				if trains[t1][0][0] == trains[t2][0][0] and trains[t1][0][1] == trains[t2][0][1]:
					print "Collision at t=", t, "and location=", trains[t1][0], "between trains", t1, "and", t2
					collided += [t1, t2]
					break
		if collided:
			trains = [trains[x] for x in xrange(0,len(trains)) if x not in collided]

		if len(trains) < 2:
			print "Last trains:", trains
			return
	print "Could not find a solution. Something is WRONG!"


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip("\n\t"), raw)
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
					tests.append(read_input(testfile))
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = read_input(sys.argv[0].replace(".py", "_input.txt"))

	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		for t in xrange(0, len(tests)):
			if enablePart1:
				print "--- Test #" + str(t+1) + ".1 ------------------------------"
				main_1(tests[t])
			if enablePart2:
				print "--- Test #" + str(t+1) + ".2 ------------------------------"
				main_2(tests[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp)