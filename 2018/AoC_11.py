import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
inp = 8561

enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def make_grid(size, serial):
	grid = []
	for y in xrange(0, size):
		row = []
		for x in xrange(0, size):
			rackID = x + 10
			power = ((rackID * y + serial) * rackID / 100) % 10 - 5
			row.append(power)
		grid.append(row)
	return grid


def main_1(inp):
	size = 300
	g = make_grid(size, inp)

	max_c = [-1, -1]
	max_p = -(1 << 63)

	b = 3
	for y in xrange(0, size-b+1):
		for x in xrange(0, size-b+1):
			s = 0

			# for t in xrange(y, y+b):
			# 	for s in xrange(x, x+b):
			# 		s += g[t][s]	

			for i in xrange(y, y+b):
				s += sum(g[i][x:x+b])	

			if s > max_p:
				max_p = s
				max_c = [x, y]

	print max_c
	

def main_2(inp):
	size = 300
	g = make_grid(size, inp)

	max_b = -1
	max_c = [-1, -1]
	max_p = -(1 << 63)

	for b in xrange(1, 300):
		print b, "..."
		for y in xrange(0, size-b+1):
			for x in xrange(0, size-b+1):
				s = 0
				for i in xrange(y, y+b):
					s += sum(g[i][x:x+b])	
				if s > max_p:
					max_p = s
					max_c = [x, y]
					max_b = b

	print max_c, max_b


if __name__ == "__main__":
	# process input
	print "--------------------------------------------------------------------------------"
	print "- INPUT"
	print "--------------------------------------------------------------------------------"
	if enablePart1:
		print "--- Part 1 ------------------------------"
		main_1(inp)
	if enablePart2:
		print "--- Part 2 ------------------------------"
		main_2(inp)