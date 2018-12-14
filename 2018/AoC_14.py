import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests1 = [9, 5, 18, 2018]
tests2 = ["51589", "01245", "92510", "59414"]

inp1 = 990941
inp2 = "990941"

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def main_1(inp):
	elves = [0, 1]
	rec = [3, 7]
	while len(rec) < inp + 9 + 1:
		# s = ""
		# for i in xrange(0, len(rec)):
		# 	if i == elves[0]:
		# 		s += "(" + format(rec[i], "2d") + ") "
		# 	elif i == elves[1]:
		# 		s += "[" + format(rec[i], "2d") +"] "
		# 	else:
		# 		s += " " + format(rec[i], "2d") + "  "
		# print s

		mix = str(sum([rec[x] for x in elves]))
		for c in mix:
			rec.append(int(c))
		for e in xrange(0, len(elves)):
			elves[e] = (elves[e] + rec[elves[e]] + 1) % len(rec)
	print "next 10 scores after recipe", inp, "are", rec[inp:inp+10]


def main_2(inp):
	elves = [0, 1]
	rec = [3, 7]
	target = inp
	length = len(inp)

	for i in xrange(0, 100000000):
		mix = str(sum([rec[x] for x in elves]))
		for c in mix:
			rec.append(int(c))
			last = "".join([str(x) for x in rec[-length:]])
			if last == target:
				print "pattern", inp, "is matched after ", len(rec) - length, "recipe(s)."
				return

		for e in xrange(0, len(elves)):
			elves[e] = (elves[e] + rec[elves[e]] + 1) % len(rec)


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

if __name__ == "__main__":
	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			for t in xrange(0, len(tests1)):
				print "--- Test #" + str(t+1) + ".1 ------------------------------"
				main_1(tests1[t])
		if enablePart2:
			for t in xrange(0, len(tests1)):
				print "--- Test #" + str(t+1) + ".2 ------------------------------"
				main_2(tests2[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp1)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp2)