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


def blinks(stones, iter):
	for _ in range(iter):
		output = []	
		for s in stones:
			if s == 0:
				output.append(1)
				continue
			txt = str(s)
			if len(txt) % 2 == 0:
				hp = int(len(txt)/2)
				output.append(int(txt[:hp]))
				output.append(int(txt[hp:]))
				continue
			output.append(2024 * s)
		stones = output
	return stones


def main_1(inp):
	stones = [int(x) for x in inp[0].split(" ")]

	stones = blinks(stones, 25)
	print(len(stones))


def blink_recursive(stone, iter, i=0, cache={}):
	count = 0
	if i == iter:
		return 1
	else:
		txt = str(stone)
		if (stone, i) in cache:
			return cache[(stone, i)]
		elif stone == 0:
			count = blink_recursive(1, iter, i+1, cache)
		elif len(txt) % 2 == 0:
			hp = int(len(txt)/2)
			count = blink_recursive(int(txt[:hp]), iter, i+1, cache) + blink_recursive(int(txt[hp:]), iter, i+1, cache)
		else:
			count = blink_recursive(2024 * stone, iter, i+1, cache)
		cache[(stone, i)] = count
		return count


def main_2(inp):
	stones = [int(x) for x in inp[0].split(" ")]

	count = 0
	for s in stones:
		count += blink_recursive(s, 75)

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