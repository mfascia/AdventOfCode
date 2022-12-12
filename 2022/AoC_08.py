import os
import sys
from PIL import Image


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


def print_grid(grid):
	txt = ""
	for row in grid:
		txt += " ".join(map(lambda x: str(x), row)) + "\n"
	print(txt)


def save_grid(grid, suffix, scale):
	sx = len(grid)
	sy = len(grid[1])
	im = Image.new(mode="RGB", size=(sx, sy))	
	for y in range(sy):
		for x in range(sx):
			c = int(scale * float(grid[y][x])) 
			im.putpixel((x, y), (c, c, c))

	filename = sys.argv[0][:-3]
	if isTest:
		filename += "-test-" + suffix + ".png"
	else:
		filename += "-input-" + suffix + ".png"

	im.save(filename)


def main_1(inp):
	sY = len(inp)
	sX = len(inp[1])

	trees = []
	for line in inp:
		row = [x for x in map(lambda x: int(x), line)]
		trees.append(row)

	save_grid(trees, "trees", 28)

	if isTest:
		print("forest:")
		print_grid(trees)	
		
	vis = [[0 for x in range(sX)] for y in range(sY)]
	for y in range(sY):
		vis[y][0] = 1
		vis[y][-1] = 1
	for x in range(sX):
		vis[0][x] = 1
		vis[-1][x] = 1

	# left edge
	for y in range(1, sY-1):
		tallest = trees[y][0]
		for x in range(1, sX-1):
			if trees[y][x] > tallest:
				vis[y][x] = 1
				tallest = trees[y][x]

	# right edge
	for y in range(1, sY-1):
		tallest = trees[y][-1]
		for x in range(sX-2, 0, -1):
			if trees[y][x] > tallest:
				vis[y][x] = 1
				tallest = trees[y][x]

	# top edge
	for x in range(1, sX-1):
		tallest = trees[0][x]
		for y in range(1, sY-1):
			if trees[y][x] > tallest:
				vis[y][x] = 1
				tallest = trees[y][x]

	# bottom edge
	for x in range(1, sX-1):
		tallest = trees[-1][x]
		for y in range(sY-2, 0, -1):
			if trees[y][x] > tallest:
				vis[y][x] = 1
				tallest = trees[y][x]

	total = 0
	for row in vis:
		total += sum(row)

	if isTest:
		print("vis map:")
		print_grid(vis)

	save_grid(trees, "vis", 255)

	print(total)


def main_2(inp):
	sY = len(inp)
	sX = len(inp[1])

	trees = []
	for line in inp:
		row = [x for x in map(lambda x: int(x), line)]
		trees.append(row)

	scenicMap = [[0 for x in range(sX)] for y in range(sY)]
	
	maxScenic = 0
	for y in range(sY):
		for x in range(sX):
			scoreL = 0
			for dx in range(x+1, sX):
				scoreL += 1
				if trees[y][dx] >= trees[y][x]:
					break
			scoreR = 0
			for dx in range(x-1, -1, -1):
				scoreR += 1
				if trees[y][dx] >= trees[y][x]:
					break
			scoreT = 0
			for dy in range(y+1, sY):
				scoreT += 1
				if trees[dy][x] >= trees[y][x]:
					break
			scoreB = 0
			for dy in range(y-1, -1, -1):
				scoreB += 1
				if trees[dy][x] >= trees[y][x]:
					break
			
			score = scoreL * scoreR * scoreT * scoreB
			scenicMap[y][x] = score
			maxScenic = max(maxScenic, score)

	if isTest:
		print("Scenic scores:")
		print_grid(scenicMap)

	save_grid(scenicMap, "scenic", 255.0/maxScenic)

	print(maxScenic)


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