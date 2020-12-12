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

	pos = [0, 0]
	angle = 0 # 0 = East, 90 = North, 180 = West, 270 = -90 = South

	for line in inp:
		action = line[0]
		value = int(line[1:])

		if action == "F":
			action = "ENWS"[int(angle/90)]		

		if action == "N":
			pos[1] += value
		elif action == "S":
			pos[1] -= value
		elif action == "E":
			pos[0] += value
		elif action == "W":
			pos[0] -= value
		elif action == "R":
			angle = (angle - value) % 360
		elif action == "L":
			angle = (angle + value) % 360

	print("final position:", pos)
	print("manhattan distance:", abs(pos[0])+abs(pos[1]))
	

def main_2(inp):
	pos = [0, 0]
	wp = [10, 1]

	for line in inp:
		action = line[0]
		value = int(line[1:])

		if action == "N":
			wp[1] += value
		elif action == "S":
			wp[1] -= value
		elif action == "E":
			wp[0] += value
		elif action == "W":
			wp[0] -= value
		elif action == "L":
			for i in range(0, value, 90):
				wp = [-wp[1], wp[0]]
		elif action == "R":
			for i in range(0, value, 90):
				wp = [wp[1], -wp[0]]
		elif action == "F":
			pos[0] += wp[0] * value
			pos[1] += wp[1] * value

	print("final position:", pos)
	print("manhattan distance:", abs(pos[0])+abs(pos[1]))


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