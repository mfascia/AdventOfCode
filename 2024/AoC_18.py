import os
import sys
import math
from collections import defaultdict
from queue import PriorityQueue

import AoC as aoc


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


MAX_TIME = 1000000


def print_grid(blocks, size, path=[]):
	lz = int(math.log10(len(blocks.keys()))) + 1

	txt = "".join([" " for x in range(lz)]) + " | "
	for x in range(size):
		txt += str(x).zfill(lz) + " "
	print(txt)
	print("".join(["-" for x in range(len(txt))]))

	for y in range(size):
		txt = str(y).zfill(lz) + " | "
		for x in range(size):
			pos = aoc.Vector(x, y)
			if pos in path:
				txt += "".join(["O" for x in range(lz)])
			elif pos in blocks and blocks[pos]<MAX_TIME:
				txt += str(blocks[pos]).zfill(lz)
			else:
				txt += "".join(["." for x in range(lz)])
			txt += " "
		print(txt)


def parse(inp):
	blocks = defaultdict(lambda:MAX_TIME)
	for i, line in enumerate(inp):
		blocks[aoc.Vector.from_list([int(x) for x in line.split(",")])] = i
	if isTest:
		size = 7
	else:
		size = 71
	bounds = [aoc.Vector(0,0), aoc.Vector(size,size)]
	return blocks, bounds, size


def pathfind(blocks, bounds, size, start, end, t0):
	open = PriorityQueue()
	costs = defaultdict(lambda:MAX_TIME)
	preds = defaultdict(lambda:None)

	costs[start] = 0
	open.put((0, start))

	path = []
	while not open.empty():
		loc = open.get()
		cost = loc[0]
		pos = loc[1]
		
		costs[pos] = cost

		if pos == end:
			while pos:
				path.append(pos)
				pos = preds[pos]
			path = path[::-1]
			return path

		for ndir in aoc.ADJ_4:
			npos = pos + ndir
			ncost = cost + 1
			btime = 0 if blocks[npos] < t0 else MAX_TIME			# filter out blocks that would land after t0
			if npos.is_inside(*bounds) and btime == MAX_TIME:
				if ncost < costs[npos]:
					preds[npos] = pos
					tup = (ncost, npos)
					if not tup in open.queue:
						open.put(tup)
	return [] 


def main_1(inp):
	blocks, bounds, size = parse(inp)
	
	start = aoc.Vector(0, 0)
	end = aoc.Vector(size-1, size-1)
	t0 = 12 if isTest else 1024
	path = pathfind(blocks, bounds, size, start, end, t0)

	# print_grid(blocks, size, path)
	# print(path)
	print(len(path)-1)


def main_2(inp):
	blocks, bounds, size = parse(inp)
	
	start = aoc.Vector(0, 0)
	end = aoc.Vector(size-1, size-1)

	# binary search the first t value that does not return a path
	tL = (12 if isTest else 1024)
	tR = len(blocks)-1
	while True:
		if tL == tR or tL == tR-1:
			break
		tM = tL + int((tR-tL)/2)
		pathM = pathfind(blocks, bounds, size, start, end, tM)
		if len(pathM) > 0:
			tL = tM
		else:
			tR = tM

	ret = [k for k,v in blocks.items() if v==(tM)]
	print(*ret)


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