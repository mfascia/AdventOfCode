import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
inp_min = 264360
inp_max = 746325

enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def main_1(inpMin, inpMax):
	passwords = []
	for i in xrange(inpMin, inpMax):
		s = str(i)
		double = False
		incr = True
		for c in xrange(0, 5):
			if s[c] == s[c+1] and double == False:
				double = True
			if s[c] > s[c+1]:
				incr = False
				break
		if double and incr:
			passwords.append(i)

	print len(passwords), passwords



def test2(i):
	s = str(i)
	double = False
	state = 0
	sub = 0
	for c in xrange(0, 5):
		if state == 0 and s[c] == s[c+1]:
			sub = 2
			state = 1
		elif state == 1: 
			if s[c] == s[c+1]:
				sub +=1
			else:
				state = 0
				if sub == 2:
					double = True
	if state == 1 and sub == 2:		
		double = True

	incr = True
	for c in xrange(0, 5):
		if s[c] > s[c+1]:
			incr = False
			break
	
	return incr and double


def main_2(inpMin, inpMax):
	passwords = []
	for i in xrange(inpMin, inpMax):
		if test2(i):
			passwords.append(i)
	print len(passwords), passwords


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

if __name__ == "__main__":
	# process input
	print "--------------------------------------------------------------------------------"
	print "- INPUT"
	print "--------------------------------------------------------------------------------"
	if enablePart1:
		print "--- Part 1 ------------------------------"
		main_1(inp_min, inp_max)
	if enablePart2:
		print "--- Part 2 ------------------------------"
		main_2(inp_min, inp_max)