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
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def parse(inp):
	diskmap = inp[0]	
	blocks = []
	filenum = 0
	files = {}
	holes = []
	pos = 0
	isFile = True
	for d in diskmap:
		size = int(d)
		if isFile:
			isFile = False
			for i in range(size):
				blocks.append(filenum)
			files[filenum] = [pos, size]
			filenum += 1
			pos += size
		else:
			isFile = True
			for i in range(size):
				blocks.append(-1)
			holes.append([pos, size])
			pos += size
	return blocks, files, holes


def main_1(inp):
	blocks, files, holes = parse(inp)
	i = 0
	j = len(blocks)-1
	while j > i+1:
		if blocks[j] != -1: 
			while blocks[i] != -1:
				i += 1
			blocks[i] = blocks[j]
			i += 1
			blocks[j] = -1
		j -= 1

	chk = 0
	for b in range(len(blocks)):
		if blocks[b] != -1:
			chk += b * blocks[b]

	# print("".join([str(x) for x in blocks]).replace("-1", "."))
	print("checksum:", chk)


def main_2(inp):
	blocks, files, holes = parse(inp)
	maxFiles = max(files.keys())
	for f in range(maxFiles, -1, -1):
		pos = files[f][0]
		size = files[f][1]
		holesToRemove = []

		for h in range(len(holes)):
			if holes[h][1] >= size and holes[h][0] < pos:
				# found a hole large enough that is left of the file we are considering
				npos = holes[h][0]
				# update the blocks
				for i in range(size):
					blocks[pos+i] = -1
					blocks[npos+i] = f
				# update file object
				files[f][0] = holes[h][0]
				# update holes list
				holes[h][1] -= size
				holes[h][0] += size
				if holes[h][1] < 1:
					holesToRemove.append(h)
				break
		holesToRemove.reverse()
		for h in holesToRemove:
			holes = holes[:h] + holes [h+1:]


	chk = 0
	for b in range(len(blocks)):
		if blocks[b] != -1:
			chk += b * blocks[b]

	# print("".join([str(x) for x in blocks]).replace("-1", "."))
	print("checksum:", chk)


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