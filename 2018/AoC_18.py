import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
verbose = False
#-----------------------------------------------------------------------------------------------


offsets = [[-1,-1], [0,-1], [1,-1], [-1,0], [1,0], [-1,1], [0,1], [1,1]]

def evolve(grid):
	w = len(grid[0])+2
	h = len(grid)+2
	
	# pad grid
	empty_line = "".join(["." for x in xrange(0,w)])
	old = [empty_line]
	old += ["." + x + "." for x in grid] 
	old.append(empty_line) 

	new = []
	for y in xrange(1, h-1):
		line = ""
		for x in xrange(1, w-1):
			c = old[y][x]
			neighbours = []
			for off in offsets:
				neighbours.append(old[y+off[1]][x+off[0]])
			if c == ".":
				if neighbours.count("|") >= 3:
					line += "|"
				else:
					line += "."
			elif c == "|":
				if neighbours.count("#") >= 3:
					line += "#"
				else:
					line += "|"
			elif c == "#":
				if neighbours.count("#") >= 1 and neighbours.count("|") >= 1:
					line += "#"
				else:
					line += "."
			else:
				print "we should never reach this!"
		
		new.append(line)
		if verbose:
			print line
	if verbose:
		print
	return new
				

def main_1(inp):
	for i in xrange(0, 10):
		inp = evolve(inp)

	states = ".#|"
	counts = [0, 0, 0]
	for y in xrange(0, len(inp)):
		for x in xrange(0,len(inp[0])):
			counts[states.index(inp[y][x])] += 1

	print "after 10 minutes, there are", counts[0], "open acres,", counts[1], "acres of trees and", counts[2], "acres of lumberyards"
	print "the total value of the lumber collection is", counts[1] * counts[2]


def main_2(inp):
	a = -1
	b = -1
	history = [inp]
	for i in xrange(1, 1000):
		match = False
		if verbose:
			print "gen", i
		inp = evolve(inp)
		for j in xrange(0, len(history)):
			if inp == history[j]:
				a = j
				b = i
				match = True
				break
		history.append(inp)
		if match:
			break

	if a == b:
		print "the output is not periodic. Giving up!"

	print "gen", a, "and", b, "match!"

	nb = 1000000000 - a
	nb = nb % (b-a)


	print "the output is periodic and we only need to compute the last", nb, "!"

	for i in xrange(0, nb):
		inp = evolve(inp)

	states = ".#|"
	counts = [0, 0, 0]
	for y in xrange(0, len(inp)):
		for x in xrange(0,len(inp[0])):
			counts[states.index(inp[y][x])] += 1

	print "after 1000000000 minutes, there are", counts[0], "open acres,", counts[1], "acres of trees and", counts[2], "acres of lumberyards"
	print "the total value of the lumber collection is", counts[1] * counts[2]


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