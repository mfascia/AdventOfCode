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
#-----------------------------------------------------------------------------------------------


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
# Directions go clockwise. Positive inc goes right, negative go left
# Note that n and S are swapped as the input is also swapped vertically
#		 N       E       S        W	
dirs = [ [0, -1], [1, 0], [0, 1], [-1, 0]]
dir_names = ["N", "E", "S", "W"]


def main_1(inp):
	off = len(inp)/2
	grid = {}
	for y in xrange(0, len(inp)):
		for x in xrange(0, len(inp[0])):
			grid[(x-off, y-off)] = inp[y][x]

	count = 0
	d = NORTH
	x = 0
	y = 0
	for b in xrange(0, 10000):
		if grid[(x,y)] == ".":
			# current pos is clean
			d = (d + 3) % 4
			grid[(x,y)] = "#"
			count += 1 
		else:
			# current pos is infected
			d = (d + 1) % 4
			grid[(x,y)] = "."

		x += dirs[d][0]
		y += dirs[d][1]
		if not grid.has_key((x,y)):
			grid[(x,y)] = "."
	print count


def main_2(inp):
	off = len(inp)/2
	grid = {}
	for y in xrange(0, len(inp)):
		for x in xrange(0, len(inp[0])):
			grid[(x-off, y-off)] = inp[y][x]

	count = 0
	d = NORTH
	x = 0
	y = 0
	for b in xrange(0, 10000000):
		if grid[(x,y)] == ".":
			# current pos is clean
			d = (d + 3) % 4	# left
			grid[(x,y)] = "w"
		elif grid[(x,y)] == "w":
			# current pos is weakened
			grid[(x,y)] = "#"
			count += 1 
		elif grid[(x,y)] == "#":
			# current pos is infected
			d = (d + 1) % 4 # right
			grid[(x,y)] = "f"
		else:
			# current pos is flagged
			d = (d + 2) % 4
			grid[(x,y)] = "."

		x += dirs[d][0]
		y += dirs[d][1]
		if not grid.has_key((x,y)):
			grid[(x,y)] = "."
	print count


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