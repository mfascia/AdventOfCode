import os
import sys
import re
from PIL import Image
from collections import deque

sys.setrecursionlimit(100000)


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = False
doInput = not doTests
printGrid = not doInput
saveImages = doInput
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------

GRID_WIDTH = 700	
GRID_HEIGHT = 2100
springPos = (500, 0)

wc = 0

def parse_input(inp):
	grid = [["." for x in xrange(0, GRID_WIDTH)] for y in xrange(0, GRID_HEIGHT)]
	
	minX = 1 << 31
	maxX = -1

	minY = 1 << 31
	maxY = -1

	for line in inp:
		if len(line)==0:
			continue
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
			minY = min(minY, c2)
			maxY = max(maxY, c3)
		else:
			#horizontal line
			for i in xrange(c2, c3+1):
				grid[c1][i] = "#"
			minX = min(minX, c2)
			maxX = max(maxX, c3)
			minY = min(minY, c1)
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


def save_image(name, grid, x, y, w, h):
	im = Image.new(mode="RGB", size=(w, h))	
	for j in xrange(y, y+h):
		for i in xrange(x, x+w):
			if grid[j][i] == "+":
				im.putpixel((i-x, j-y), (255, 0, 0))
			elif grid[j][i] == "~":
				im.putpixel((i-x, j-y), (0, 0, 255))
			elif grid[j][i] == "|":
				im.putpixel((i-x, j-y), (0, 255, 255))
			elif grid[j][i] == ".":
				im.putpixel((i-x, j-y), (127, 127, 127))
			else:
				im.putpixel((i-x, j-y), (0, 0, 0))
	im.save(name)



def water_source(grid, bbox, x, y):
	# global wc 
	# wc += 1
	# if wc > 300:
	# 	return

	# drop flowing water vertically
	while grid[y][x] in ".|":
		if grid[y][x] == "|":
			return
		grid[y][x] = "|"
		y += 1
		# kill the flow if we reached the bottom
		if y > bbox[3]:
			return

	watertight = True
	sources = []
	while watertight and y >= 0:
		y -= 1		

		# search left for either a hole or a wall
		l = 0
		for i in xrange(x-1, -1, -1):
			if grid[y][i] == "#":			
				l = i+1
				break
			elif grid[y+1][i] in ".|":
				# found a hole, start a source there
				l = i
				sources.append([i, y+1])
				watertight = False
				break
			
		# search left for either a hole or a wall
		r = GRID_WIDTH-1
		for i in xrange(x+1, GRID_WIDTH):
			if grid[y][i] == "#":
				r = i-1
				break
			elif grid[y+1][i] in ".|":
				# found a hole, start a source there
				r = i
				sources.append([i, y+1])
				watertight = False
				break

		# add a row of stable water if watertight or flowing water if not
		for i in xrange(l, r+1):
			grid[y][i] = "~" if watertight else "|"
		
		if printGrid:
			print_grid(grid, x, y, bbox[0]-1, bbox[1], bbox[2]-bbox[0]+3, bbox[3]-bbox[1]+1)

		# do any additional sources
		for s in sources:
			water_source(grid, bbox, s[0], s[1])


def main(inp):
	grid, bbox = parse_input(inp)
	
	print bbox

	if saveImages:
		save_image(sys.argv[0].replace(".py", "_initial.png"), grid, bbox[0]-50, 0, bbox[2]-bbox[0]+1+100, bbox[3]-bbox[1]+1+50)

	water_source(grid, bbox, springPos[0], springPos[1])

	if printGrid:
		print_grid(grid, 0, 0, bbox[0]-1, bbox[1], bbox[2]-bbox[0]+3, bbox[3]-bbox[1]+1)

	reachable = 0
	stable = 0
	for y in xrange(bbox[1], bbox[3]+1):
		for x in xrange(0, GRID_WIDTH):
			if grid[y][x] == "|":
				reachable += 1
			elif grid[y][x] == "~":
				reachable += 1
				stable += 1

	print "water reached", reachable, "cell(s)"
	print "only", stable, "volume(s) of water are stable"

	if saveImages:
		save_image(sys.argv[0].replace(".py", "_final.png"), grid, bbox[0]-50, 0, bbox[2]-bbox[0]+1+100, bbox[3]-bbox[1]+1+50)


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
			print "--- Test #" + str(t+1) + " ------------------------------"
			main(tests[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		main(inp)