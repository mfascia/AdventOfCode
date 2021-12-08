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


def main_1(inp):
	count = 0
	for line in inp:
		left, right = line.split(" | ")
		easyDigits = [x for x in right.split(" ") if len(x) not in [5,6]]
		count += len(easyDigits)

	print(count)


def shuffleAlphabetical(signal):
	tmp = list(signal)
	tmp.sort()
	return "".join(tmp)

def strdif(a, b):
	ret = ""
	for i in a:
		if i not in b:
			ret += i
	for i in b:
		if i not in a and i not in ret:
			ret += i
	return ret


def decode(signals):
	sizes = [[] for x in range(0, 8)]
	digits = ["" for x in range(0, 10)] 

	for s in signals:
		sizes[len(s)].append(s)
	
	# identify the trivial digits
	digits[1] = sizes[2][0]
	digits[4] = sizes[4][0]
	digits[7] = sizes[3][0]
	digits[8] = sizes[7][0]

	# find "3". It is the only 5 segment digit with 2 segments different from "7"
	for s in sizes[5]:
		if len(strdif(s, digits[7])) == 2:
			digits[3] = s
			sizes[5].remove(s)
			break
	
	# find "9". It is the only 6 segments digit with 1 segments different from "3"
	for s in sizes[6]:
		if len(strdif(s, digits[3])) == 1:
			digits[9] = s
			sizes[6].remove(s)
			break
	
	# find 0. It is the only 6 segments digit with 3 segments different from "7"
	for s in sizes[6]:
		if len(strdif(s, digits[7])) == 3:
			digits[0] = s
			sizes[6].remove(s)
			break
	
	# deduce "6"
	digits[6] = sizes[6][0]

	# find "5". It is the only 5 segments digit with 1 segments different from "6"
	for s in sizes[5]:
		if len(strdif(s, digits[6])) == 1:
			digits[5] = s
			sizes[5].remove(s)
			break
		
	# deduce "2"
	digits[2] = sizes[5][0]

	return digits


def main_2(inp):
	data = []
	total = 0
	for line in inp:
		left, right = line.split(" | ")
		d = [[shuffleAlphabetical(x) for x in left.split(" ")], [shuffleAlphabetical(x) for x in right.split(" ")]]
		lut = decode(d[0])
		val = ""
		for n in d[1]:
			val += str(lut.index(n))
		total += int(val)
	
	print(total)


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