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

def processInput(inp):
	numbers = [int(x) for x in inp[0].split(",")]

	inp = inp [2:]
	boards = []
	b = []
	for line in inp:
		if len(line) == 0:	
			boards.append(b)
			b = []
		else:
			b = b + [int(x) for x in line.strip().replace("  ", " ").split(" ")]
	boards.append(b)
	return numbers, boards

def printBoards(boards):
	for b in boards:
		s = ""
		for i in range(0, 25):
			if i>0 and i % 5 == 0:
				print(s)
				s = ""
			if b[i] == "#":
				s += "##   "
			else:
				s += "{: >2d}   ".format(b[i])
		print(s)
		print()

def checkBoard(board):
	for i in range(0, 5):
		line = 0
		column = 0
		for k in range(0, 5):
			if board[5*i+k] == "#":
				line += 1
			if board[5*k + i] == "#":
				column += 1
		if line == 5 or column == 5:
			return True 
	return False

def calcScore(board, n):
	s = 0
	for v in board:
		if v != "#":
			s += int(v)
	return s*n



def main_1(inp):
	numbers, boards = processInput(inp)

	for n in numbers:
		for i in range(0, len(boards)):
			for j in range(0, 25):
				if boards[i][j] == n:
					boards[i][j] = "#"

		for i in range(0, len(boards)):
			if checkBoard(boards[i]):
				print(calcScore(boards[i], n))
				return



def main_2(inp):
	numbers, boards = processInput(inp)
	winners = []
	winvals = []
	for n in numbers:
		for i in range(0, len(boards)):
			for j in range(0, 25):
				if boards[i][j] == n:
					boards[i][j] = "#"
		toRemove = []
		for i in range(0, len(boards)):
			if checkBoard(boards[i]):
				toRemove.append(i)
		toRemove.sort(reverse=True)
		for i in toRemove:
			winners.append(boards.pop(i))
			winvals.append(n)

	print(calcScore(winners[len(boards)-1], winvals[len(winvals)-1]))



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