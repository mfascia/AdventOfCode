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

# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors

MOVES_1 = {
	"A X": 4,	# Rock 		Rock		DRAW	1 + 3
	"A Y": 8,	# Rock		Paper		WIN		2 + 6
	"A Z": 3,	# Rock		Scissors	LOSS	3 + 0
	"B X": 1,	# Paper		Rock		LOSS	1 + 0
	"B Y": 5,	# Paper		Paper		DRAW	2 + 3
	"B Z": 9,	# Paper		Scissors	WIN		3 + 6
	"C X": 7,	# Scissors	Rock		WIN		1 + 6
	"C Y": 2,	# Scissors	Paper		LOSS	2 + 0
	"C Z": 6,	# Scissors	Scissors	DRAW	3 + 3
}

def main_1(inp):
	score = 0
	for move in inp:
		s = MOVES_1[move]
		#print(move, s)
		score += s

	print(score)

# A for Rock, B for Paper, and C for Scissors
# X for Loss, Y for Draw, and Z for Win

MOVES_2 = {
	"A X": 3,	# Rock 		Scissors	LOSS	3 + 0
	"A Y": 4,	# Rock		Rock		DRAW	1 + 3
	"A Z": 8,	# Rock		Paper		WIN		2 + 6
	"B X": 1,	# Paper		Rock		LOSS	1 + 0
	"B Y": 5,	# Paper		Paper		DRAW	2 + 3
	"B Z": 9,	# Paper		Scissors	WIN		3 + 6
	"C X": 2,	# Scissors	Paper		LOSS	2 + 0
	"C Y": 6,	# Scissors	Scissors	DRAW	3 + 3
	"C Z": 7,	# Scissors	Rock		WIN		1 + 6
}


def main_2(inp):
	score = 0
	for move in inp:
		s = MOVES_2[move]
		#print(move, s)
		score += s

	print(score)


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