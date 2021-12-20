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
enablePart2 = False
#-----------------------------------------------------------------------------------------------

NEIGHBOURS = [[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
PAD = 20


def enhance(image, algo, iter):
	sx = len(image[0])
	sy = len(image)
	enhanced = [[0 for x in range(sx)] for y in range(sy)]
	for y in range(sy):
		for x in range(sx):
			neighbours = [n for n in map(lambda k: [x+k[0], y+k[1]], NEIGHBOURS) if n[0]>=0 and n[0]<sx and n[1]>=0 and n[1]<sy]
			bits = []
			for n in neighbours:
				bits.append(image[n[1]][n[0]])
			lookup = int( "".join([str(b) for b in bits]),2)
			enhanced[y][x] = algo[lookup]
	return enhanced


def print_image(image):
	for row in image:
		print("".join(["#" if x == 1 else "." for x in row]))
	print



def main_1(inp):
	algo = [1 if x == "#" else 0 for x in inp[0]]
	
	image = []
	for line in inp[2:]:
		row = []
		for c in line:
			row.append(1 if c == "#" else 0)
		image.append([0 for x in range(PAD)] + row + [0 for x in range(PAD)])
	
	for p in range(PAD):
		image.append([0 for x in range(len(image[0]))])
	for p in range(PAD):
		image.insert(0, [0 for x in range(len(image[0]))])

	for i in range(2):
		temp = enhance(image, algo, i)
		image = temp

	lit = sum([sum(row[1:-1]) for row in image[1:-1]])
	print("lit pixels:", lit)


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