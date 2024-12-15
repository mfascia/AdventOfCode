import os
import sys
import AoC as aoc


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


def solution(inp, offset):
	tokens = 0
	k = 0
	while k < len(inp):
		tax, tay = inp[k][9:].split(", ")
		tbx, tby = inp[k+1][9:].split(", ")
		tpx, tpy = inp[k+2][7:].split(", ")

		# This can be expressed as a system of 2 equations with 2 varaibles i and j:
		# 	{ x = ai + cj
		# 	{ y = bi + dj
		# and with a bit of algebra we get:
		# 	j = (ay-cx)/(ad-bc)
		# 	i = x/a - cj/a
		# if i and j are integers, we have a match!
		a = int(tax[2:])
		b = int(tay[2:])
		c = int(tbx[2:])
		d = int(tby[2:])
		x = int(tpx[2:]) + offset
		y = int(tpy[2:]) + offset

		j = (a*y - b*x) / (a*d  - b*c) 
		i = (x - c*j) / a

		if i.is_integer() and j.is_integer():
			tokens += 3*i + j

		k += 4
	print(tokens)

def main_1(inp):
	solution(inp, 0)

def main_2(inp):
	solution(inp, 10000000000000)


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