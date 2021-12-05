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


def main(inp, skip_diagonals):
	lines = []
	vents = {}
	for line in inp:
		s, e = line.split(" -> ")
		l = [[int(x) for x in s.split(",")], [int(x) for x in e.split(",")]]
		lines.append(l)

		# skip diagonals for part 1
		if skip_diagonals and l[0][0] != l[1][0] and l[0][1] != l[1][1]:
			continue

		# calculate which way to move along the X axis
		if l[1][0] > l[0][0]:
			dx = 1
		elif l[1][0] < l[0][0]:
			dx = -1
		else:
			dx = 0

		# calculate which way to move along the Y axis
		if l[1][1] > l[0][1]:
			dy = 1
		elif l[1][1] < l[0][1]:
			dy = -1
		else:
			dy = 0

		# walk the line 
		x = l[0][0]
		y = l[0][1]
		while x != l[1][0] or y != l[1][1]:
			p = str([x, y])
			if p in vents:
				vents[p] += 1
			else:
				vents[p] = 1
			x += dx
			y += dy

		# add last point			
		p = str([x, y])
		if p in vents:
			vents[p] += 1
		else:
			vents[p] = 1
		
	# sum any vent location that has been hit at least twice
	count = 0
	for val in vents.values():
		if val > 1:
			count += 1

	print(count)


def main_1(inp):
	main(inp, True)


def main_2(inp):
	main(inp, False)


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