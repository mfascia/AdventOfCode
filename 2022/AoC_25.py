import os
import sys
import math

# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------


def snafu2dec(s):
	rs = reversed(s)
	p = 1
	v = 0
	for d in rs:
		if d == '-':
			m = -1
		elif d == "=":
			m = -2
		else:
			m = int(d)
		v += m*p
		p *= 5
	return v


POWERS = [x for x in map(lambda v: 5**v, range(0, 50))]


def dec2snafu(d):
	i=0
	while d > POWERS[i]:
		i += 1

	b5 = []
	for j in range(i, -1, -1):
		p = POWERS[j]
		m = int(d / p) 
		b5.append(m)
		d = d % p
	
	s = ""
	b5r = [x for x in reversed(b5)]
	for i in range(len(b5r)):
		if b5r[i] > 4:
			b5r[i+1] += int(b5r[i]/5)
			b5r[i] = b5r[i] % 5
		if b5r[i] < 3:
			s += str(b5r[i])
		elif b5r[i] == 3:
			s += "="
			b5r[i+1] += 1 
		elif b5r[i] == 4:
			s += "-"
			b5r[i+1] += 1 

	if s[-1] == "0":
		s = s[0:-1]
		
	return "".join([x for x in reversed(s)])
			


def main_1(inp):
	s = 0
	for line in inp:
		dec = snafu2dec(line)
		s += dec
		snafu = dec2snafu(s)
		print(line, ">>>", dec, ">>>", snafu)
	
	snafu = dec2snafu(s)
	print("--------------------------")
	print(snafu, ">>>", s)


def main_2(inp):
	pass


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