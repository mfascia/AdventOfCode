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
enablePart2 = False
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
		pos = [line.index(x) for x in "<>^v" if x in line]
		for p in pos:
			trains.append([[p, y], line[p], 0])
			line = line[:p] + ("|" if line[p] in "v^" else "-") + line[p+1:]
		tracks.append(line)
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
		if t>0 and t%10==0:
			print t, "..."

		t += 1
		for train in trains:
			train = move(tracks, train)

		for t1 in xrange(0, len(trains)-1):
			for t2 in xrange(t1+1, len(trains)):
				if trains[t1][0][0] == trains[t2][0][0] and trains[t1][0][1] == trains[t2][0][1]:
					print "Collision at t=", t, "and location=", trains[t1][0], "between trains", t1, "and", t2
					#save_state(t, tracks, trains)
					return


def main_2(inp):
	pass


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