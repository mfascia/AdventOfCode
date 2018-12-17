import os
import sys
import re
from PIL import Image
from collections import deque


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = False
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------

GRID_WIDTH = 600
GRID_HEIGHT = 300

springPos = (500, 0)


def parse_input(inp):
	grid = [["." for x in xrange(0, GRID_WIDTH)] for y in xrange(0, GRID_HEIGHT)]
	
	minX = 1 << 31
	maxX = -1

	minY = 0
	maxY = -1

	for line in inp:
		matches = re.match("(x|y)=([0-9]*), (x|y)=([0-9]*)..([0-9]*)", line)
		a1 = matches.group(1)
		c1 = int(matches.group(2))
		a2 = matches.group(3)
		c2 = int(matches.group(4))
		c3 = int(matches.group(5))
		if a1 == "x":
			#vertical line
			for i in xrange(c2, c3+1):
				grid[i][c1] = "#"
			minX = min(minX, c1)
			maxX = max(maxX, c1)
			maxY = max(maxY, c3)
		else:
			#horizontal line
			for i in xrange(c2, c3+1):
				grid[c1][i] = "#"
			minX = min(minX, c2)
			maxX = max(maxX, c3)
			maxY = max(maxY, c1)
	
	return grid, (minX, minY, maxX, maxY)


def print_grid(grid, px, py, x, y, w, h):
	for j in xrange(y, y+h):
		line = ""
		for i in xrange(x, x+w):
			if (i, j) == (px, py):
				line += "X"
			else:
				line += grid[j][i]
		print line
	print


def save_image(name, grid, sources, x, y, w, h):
	im = Image.new(mode="RGB", size=(w, h))	
	for j in xrange(y, y+h):
		for i in xrange(x, x+w):
			if grid[j][i] == "+":
				im.putpixel((i-x, j-y), (255, 0, 0))
			elif grid[j][i] in "|~":
				im.putpixel((i-x, j-y), (0, 0, 255))
			elif grid[j][i] == ".":
				im.putpixel((i-x, j-y), (127, 127, 127))
			else:
				im.putpixel((i-x, j-y), (0, 0, 0))
	im.save(name)


def main_1(inp):
	grid, bbox = parse_input(inp)
	
	print bbox

	#save_image(sys.argv[0].replace(".py", "_initial.png"), grid, sources, bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1])

	water = deque()
	water.append(springPos)

	fork = deque()

	while water:
		x, y = water[len(water)-1]
		print_grid(grid, x, y, bbox[0]-1, bbox[1], bbox[2]-bbox[0]+3, bbox[3]-bbox[1]+1)

		if y == bbox[3]:
			water.pop()
			f = fork.pop()
			while water[len(water)-1] != f:
				water.pop()
			continue

		if grid[y+1][x] == ".":
			grid[y+1][x] = "|"
			water.append((x, y+1))
			continue
		elif grid[y][x-1] == ".":
			grid[y][x-1] = "|"
			water.append((x-1, y))
			fork.append((x, y))
			continue
		elif grid[y][x+1] == ".":
			grid[y][x+1] = "|"
			water.append((x+1, y))
			continue
		else:
			water.pop()




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