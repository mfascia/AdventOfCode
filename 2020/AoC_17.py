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


def printGrid3D(grid):
	line = ""
	for z in range(0, len(grid)):
		frag = "z=" + str(z)
		frag = frag + "".join([" " for x in range(len(frag), len(grid)+1)])
		line += frag
	print(line)
	for y in range(0, len(grid)):
		line = ""
		for z in range(0, len(grid)):
			line += " " + "".join(grid[z][y])
		print(line)
	print(line)


def main_1(inp):
	steps = 6
	dim = len(inp[0]) + 2*steps + 2

	grid = [[["." for x in range(0, dim)] for y in range(0, dim)] for z in range(0, dim)]
	grid2 = [[["." for x in range(0, dim)] for y in range(0, dim)] for z in range(0, dim)]
	z = steps + 1
	y = steps + 1
	for line in inp:
		x = steps + 1
		for c in line:
			grid[z][y][x] = c 
			x += 1
		y += 1

	for step in range(0, steps):
		for z in range(1, dim-1):
			for y in range(1, dim-1):
				for x in range(1, dim-1):
					count = 0
					for k in range(z-1, z+2):
						for j in range(y-1, y+2):
							for i in range(x-1, x+2):
								if i == x and j == y and k == z:
									continue
								if grid[k][j][i] == "#":
									count += 1
					if grid[z][y][x] == "#" and count != 2 and count != 3:
						grid2[z][y][x] = "."
					elif grid[z][y][x] == "." and count == 3:
						grid2[z][y][x] = "#"
					else:
						grid2[z][y][x] = grid[z][y][x]
		tmp = grid
		grid = grid2
		grid2 = tmp

	count = 0
	for z in range(1, dim-1):
		for y in range(1, dim-1):
			for x in range(1, dim-1):
				if grid[z][y][x] == "#":
					count += 1

	print(count)


def main_2(inp):
	steps = 6
	dim = len(inp[0]) + 2*steps + 2

	grid = [[[["." for x in range(0, dim)] for y in range(0, dim)] for z in range(0, dim)] for w in range(0, dim)]
	grid2 = [[[["." for x in range(0, dim)] for y in range(0, dim)] for z in range(0, dim)] for w in range(0, dim)]
	w = steps + 1
	z = steps + 1
	y = steps + 1
	for line in inp:
		x = steps + 1
		for c in line:
			grid[w][z][y][x] = c 
			x += 1
		y += 1

	for step in range(0, steps):
		for w in range(1, dim-1):
			for z in range(1, dim-1):
				for y in range(1, dim-1):
					for x in range(1, dim-1):
						count = 0
						for l in range(w-1, w+2):
							for k in range(z-1, z+2):
								for j in range(y-1, y+2):
									for i in range(x-1, x+2):
										if i == x and j == y and k == z and l == w:
											continue
										if grid[l][k][j][i] == "#":
											count += 1
						if grid[w][z][y][x] == "#" and count != 2 and count != 3:
							grid2[w][z][y][x] = "."
						elif grid[w][z][y][x] == "." and count == 3:
							grid2[w][z][y][x] = "#"
						else:
							grid2[w][z][y][x] = grid[w][z][y][x]
		tmp = grid
		grid = grid2
		grid2 = tmp

	count = 0
	for w in range(1, dim-1):
		for z in range(1, dim-1):
			for y in range(1, dim-1):
				for x in range(1, dim-1):
					if grid[w][z][y][x] == "#":
						count += 1

	print(count)



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
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)