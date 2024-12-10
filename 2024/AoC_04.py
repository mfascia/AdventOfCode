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
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------

def scan_xmas(puzzle, word, width, height, dx, dy):
	count = 0
	x = 0
	y = 0
	minx = len(word)-1 if dx<0 else 0
	maxx = width - (len(word)-1 if dx>0 else 0)
	miny = len(word)-1 if dy<0 else 0
	maxy = height - (len(word)-1 if dy>0 else 0)
	for y in range(miny, maxy):
		for x in range(minx, maxx):
			text = ""
			for i in range(len(word)):
				sx = x+dx*i
				sy = y+dy*i
				text += puzzle[sy][sx]
			if text == word:
				count += 1
	return count
		

def main_1(inp):
	width = len(inp[0])
	height = len(inp)

	count = 0
	dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1,-1], [-1, 1], [-1, -1]]
	for d in dirs:	
		count += scan_xmas(inp, "XMAS", width, height, *d)
	print(count)


def main_2(inp):
	count = 0
	width = len(inp[0])
	height = len(inp)
	for y in range(1, height-1):
		for x in range(1, width-1):
			if inp[y][x] != "A":
				continue
			d1 = "" + inp[y-1][x-1] + inp[y][x] + inp[y+1][x+1]
			d2 = "" + inp[y+1][x-1] + inp[y][x] + inp[y-1][x+1]
			if d1 in ["MAS", "SAM"] and d2 in ["MAS", "SAM"]:
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