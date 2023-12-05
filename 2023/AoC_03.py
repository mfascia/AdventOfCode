import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
#-----------------------------------------------------------------------------------------------

def bump_symbol(symbols, x, y, v):
	h = 10000*y + x
	if h not in symbols.keys():
		symbols[h] = [1, v, [v]]
	else:
		symbols[h][0] += 1
		symbols[h][1] *= v
		symbols[h][2].append(v)


def main(inp):
	grid = []
	symbols = {}
	grid.append("".join(["." for x in range(len(inp[0])+2)]))
	for line in inp:
		grid.append("." + line + ".")
	grid.append("".join(["." for x in range(len(inp[0])+2)]))

	sum1 = 0
	for y in range(1, len(grid)):
		in_num = False
		xs = 0
		xe = 0
		for x in range(1, len(grid[0])):
			if grid[y][x] in "0123456789":
				if not in_num:
					xs = x
					num = ""
					in_num = True
				if in_num:
					num += grid[y][x]
			else:
				if in_num:
					xe = x
					in_num = False
					added = False
					if grid[y][x] != ".":
						sum1 += int(num)
						bump_symbol(symbols, x, y, int(num))
						continue
					else:
						if grid[y][xs-1] not in "0123456789.":
							sum1 += int(num)
							bump_symbol(symbols, xs-1, y, int(num))
						else:
							for xx in range(xs-1, xe+1):
								if grid[y-1][xx] not in "0123456789.":
									sum1 += int(num)
									bump_symbol(symbols, xx, y-1, int(num))
									break
								elif grid[y+1][xx] not in "0123456789.":
									sum1 += int(num)
									bump_symbol(symbols, xx, y+1, int(num))
									break
	
	sum2 = 0
	for k, v in symbols.items():
		if v[0] > 1:
			print(k, v)
			sum2 += v[1]

	print("Part 1:", sum1)
	print("Part 2:", sum2)


# 66702420 too low

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
			print ("--- Test #" + str(t+1) + "---------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		main(inp)
