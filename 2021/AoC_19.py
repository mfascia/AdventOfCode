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
#-----------------------------------------------------------------------------------------------


XFS = [
	[ [0, 1, 2], 	[1, 1, 1] ],
	[ [1, 0, 2], 	[-1, 1, 1] ],
	[ [0, 1, 2],	[-1, -1, 1,] ],
	[ [1, 0, 2],	[1, -1, 1,] ],

	[ [2, 0, 1],	[1, 1, 1] ],
	[ [0, 2, 1],	[-1, 1, 1] ],
	[ [2, 0, 1],	[-1, -1, 1] ],
	[ [0, 2, 1],	[1, -1, 1] ],

	[ [1, 2, 0],	[1, 1, 1] ],
	[ [2, 1, 0],	[-1, 1, 1] ],
	[ [1, 2, 0],	[-1, -1, 1] ],
	[ [2, 1, 0],	[1, -1, 1] ],

	[ [2, 1, 0],	[1, 1, -1] ],
	[ [1, 2, 0],	[-1, 1, -1] ],
	[ [2, 1, 0],	[-1, -1, -1] ],
	[ [1, 2, 0],	[1, -1, -1] ],

	[ [1, 0, 2],	[1, 1, -1] ],
	[ [0, 1, 2],	[-1, 1, -1] ],
	[ [1, 0, 2],	[-1, -1, -1] ],
	[ [0, 1, 2],	[1, -1, -1] ],

	[ [0, 2, 1],	[1, 1, -1] ],
	[ [2, 0, 1],	[-1, 1, -1] ],
	[ [0, 2, 1],	[-1, -1, -1] ],
	[ [2, 0, 1],	[1, -1, -1] ]
]


def offset_scanner(scanner, offset):
	return [b for b in map(lambda x: [x[0]+ offset[0], x[1]+offset[1], x[2]+offset[2]], scanner)]

def square_dist(a, b):
	dx = b[0] - a[0]
	dy = b[1] - a[1]
	dz = b[2] - a[2]
	return dx*dx + dy*dy + dz*dz


def manhattan_dist(a, b):
	return max(a[0], b[0])-min(a[0], b[0]) + max(a[1], b[1])-min(a[1], b[1]) + max(a[2], b[2])-min(a[2], b[2])


def transform_scanner(scanner, xf):
	xbs = []
	for b in scanner:
		xbs.append([int(b[xf[0][0]] * xf[1][0]), int(b[xf[0][1]] * xf[1][1]), int(b[xf[0][2]] * xf[1][2])])
	return xbs


def match(beacons, positions, scanner):
	for xf in XFS:
		distHist = {}
		maxH = 0
		xb = transform_scanner(scanner, xf)
		for b in beacons:
			for p in xb:
				d = square_dist(b, p)
				if d in distHist:
					distHist[d] += 1
				else:
					distHist[d]	= 1	
				maxH = max(maxH, distHist[d])
		# a match mean that there are at least 12 points in this transformed data that are at the same distance from their already identified beacons 
		if maxH >= 12:
			# find the common dist
			for k,v in distHist.items():
				if v == maxH:
					break
			# find 2 points that have that dist and calculate delta
			delta = []
			for b in beacons:
				found = False
				for p in xb:
					d = square_dist(b, p)
					if d == k:
						delta = [b[0]-p[0], b[1]-p[1], b[2]-p[2]]
						positions.append(delta)
						found = True
						break
				if found:
					break
			# offset the beacons of the scanner by delta and add them to the set of known beacons
			offset = offset_scanner(xb, delta)
			for o in offset:
				if o not in beacons:
					beacons.append(o)
			return True

	return False


def main(inp):
	scanners = []
	for line in inp:
		if line.startswith("---"):
			scanner = []
		elif len(line):
			scanner.append([int(x) for x in line.split(",")])
		else:
			scanners.append(scanner)
	scanners.append(scanner)

	unmatched = [s for s in scanners[1:]]
	matched = [scanners[0]]
	beacons = [x for x in scanners[0]]
	positions = [[0, 0, 0]]
	while len(matched) < len(scanners):
		i = 0
		while i < len(unmatched):
			if match(beacons, positions, unmatched[i]):
				s = unmatched.pop(i)
				matched.append(s)
			else:
				i += 1
	print("Unique Beacons:", len(beacons))

	maxM = 0
	for s1 in positions:
		for s2 in positions:
			maxM = max(maxM, manhattan_dist(s1, s2))
	print("Max Manhattan:", maxM)


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
			print ("--- Test #" + str(t+1) + "---------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		main(inp)