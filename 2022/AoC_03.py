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
	prios = 0
	for sack in inp:
		l = sack[:int(len(sack)/2)]
		r = sack[int(len(sack)/2):]
		common = ""
		found = False
		for c in l:
			if c in r: 
				common = c
				found = True
			if found:
				break
		if common != "":
			if common.islower():
				p = ord(common) - ord("a") + 1
			else:
				p = ord(common.lower()) - ord("a") + 1 + 26
			#print(l, r, common, p)
			prios += p
		else:
			print(l, r, common, 0)

	print(prios)


def main_2(inp):
	prios = 0
	g = 0
	while g < len(inp):
		common = ""
		shortlist = []
		for c in inp[g]:
			if c in inp[g+1]:
				shortlist.append(c)
		for c in shortlist:
			if c in inp[g+2]:
				common = c
				break

		if common.islower():
			p = ord(common) - ord("a") + 1
		else:
			p = ord(common.lower()) - ord("a") + 1 + 26
		#print(inp[g])
		#print(inp[g+1])
		#print(inp[g+2])
		#print(common, p)
		prios += p

		g += 3
		
	print(prios)
			


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