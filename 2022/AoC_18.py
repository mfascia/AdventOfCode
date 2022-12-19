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
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


NEIGHBOURS = [
	[-1, 0, 0],
	[+1, 0, 0],
	[0, -1, 0],
	[0, +1, 0],
	[0, 0, -1],
	[0, 0, +1]
]

def read_lava(inp):
	lava = {}
	for line in inp:
		p = tuple([int(x) for x in line.split(",")])
		lava[p] = 6
	return lava	


def calc_bbox(cubes, padding=0):
	inf = [1000, 1000, 1000]
	sup = [-1000, -1000, -1000]
	for p in cubes.keys():
		inf[0] = min(inf[0], p[0])
		inf[1] = min(inf[1], p[1])
		inf[2] = min(inf[2], p[2])
		sup[0] = max(sup[0], p[0])
		sup[1] = max(sup[1], p[1])
		sup[2] = max(sup[2], p[2])
	inf = [v-padding for v in inf]
	sup = [v+padding for v in sup]
	return [tuple(inf), tuple(sup)]


def main_1(inp):
	lava = read_lava(inp)
	for p in lava.keys():
		for n in NEIGHBOURS:
			 if (p[0]+n[0], p[1]+n[1], p[2]+n[2]) in lava:
				 lava[p] -= 1

	surface = sum(lava.values())
	print(surface)


def main_2(inp):
	lava = read_lava(inp)
	bbox = calc_bbox(lava, 1)

	# Create a cube around the lava blob with at least 1 unit of air around it so that the floodfill can complete
	# Floodfill it with steam
	# Then look at which lava cubes' faces touch a steam cube and add them

	added = [bbox[0]]
	steam = { bbox[0]: 0 }
	i = 0
	while i<len(added):
		p = added[i]
		neighbours = [tuple(n) for n in map(lambda k: (p[0]+k[0], p[1]+k[1], p[2]+k[2]), NEIGHBOURS) if n[0]>=bbox[0][0] and n[0]<=bbox[1][0] and n[1]>=bbox[0][1] and n[1]<=bbox[1][1] and n[2]>=bbox[0][2] and n[2]<=bbox[1][2]]
		for n in neighbours:
			if n not in lava:
				if n not in steam:
					added.append(n)
					steam[n] = 0
		i += 1

	surface = 0
	for p in lava.keys():
		for n in NEIGHBOURS:
				if (p[0]+n[0], p[1]+n[1], p[2]+n[2]) in steam:
					surface += 1

	print(surface)


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