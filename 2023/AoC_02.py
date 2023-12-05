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


def main_1(inp):
	sum = 0
	for line in inp:
		#		 R  G  B
		shown = [0, 0, 0]
		game_name, all_sets = line.split(":")
		game = int(game_name[5:])
		sets = all_sets.split(";")
		for set in sets:
			cubes = set.split(",")
			for cube in cubes:
				if "red" in cube:
					shown[0] = max(shown[0], int(cube[:-3]))
				elif "green" in cube:
					shown[1] = max(shown[1], int(cube[:-5]))
				if "blue" in cube:
					shown[2] = max(shown[2], int(cube[:-4]))

		if shown[0] <= 12 and shown[1] <= 13 and shown[2] <= 14:
			sum += game

		print(game, shown, line)

	print(sum)

def main_2(inp):
	sum = 0
	for line in inp:
		#		 R  G  B
		shown = [0, 0, 0]
		game_name, all_sets = line.split(":")
		game = int(game_name[5:])
		sets = all_sets.split(";")
		for set in sets:
			cubes = set.split(",")
			for cube in cubes:
				if "red" in cube:
					shown[0] = max(shown[0], int(cube[:-3]))
				elif "green" in cube:
					shown[1] = max(shown[1], int(cube[:-5]))
				if "blue" in cube:
					shown[2] = max(shown[2], int(cube[:-4]))

		sum += shown[0] * shown[1] * shown[2]

		print(game, shown, line)

	print(sum)


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