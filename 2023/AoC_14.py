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


def parse_platform(text):
	platform = []
	for line in text:
		platform.append([c for c in line])
	return platform


def print_platform(platform):
	for line in platform:
		text = "".join(line)
		print(text)
	print()


def tilt(platform, direction):
	w = len(platform[0])
	h = len(platform)
	match direction:
		case "N":
			for y in range(1, h):
				for x in range(w):
					if platform[y][x] == "O":
						ny = y-1
						while ny >= 0 and platform[ny][x] == ".":
							ny -= 1
						platform[y][x] = "."
						platform[ny+1][x] = "O"
		case "S":
			for y in range(h-1, -1, -1):
				for x in range(w):
					if platform[y][x] == "O":
						ny = y+1
						while ny < h and platform[ny][x] == ".":
							ny += 1
						platform[y][x] = "."
						platform[ny-1][x] = "O"
		case "W":
			for x in range(1, w):
				for y in range(h):
					if platform[y][x] == "O":
						nx = x-1
						while nx >= 0 and platform[y][nx] == ".":
							nx -= 1
						platform[y][x] = "."
						platform[y][nx+1] = "O"
		case "E":
			for x in range(w-1, -1, -1):
				for y in range(h):
					if platform[y][x] == "O":
						nx = x+1
						while nx < w and platform[y][nx] == ".":
							nx += 1
						platform[y][x] = "."
						platform[y][nx-1] = "O"
	

def calc_load(platform):
	load = 0
	w = len(platform[0])
	h = len(platform)
	for y in range(0, h):
		for x in range(w):
			if platform[y][x] == "O":
				load += h - y
	return load


def platform_checksum(platform):
	sum = 0
	w = len(platform[0])
	h = len(platform)
	for y in range(0, h):
		for x in range(w):
			if platform[y][x] == "O":
				sum += 1000 * y + x
	return sum


def main_1(inp):
	platform = parse_platform(inp)
	tilt(platform, "N")
	load = calc_load(platform)
	print("Part 1: load on North beam =", load)


def main_2(inp):
	checksums = []
	loads = []
	platform = parse_platform(inp)
	cycle = -1
	chk = 0
	while True:
		cycle += 1
		tilt(platform, "N")
		tilt(platform, "W")
		tilt(platform, "S")
		tilt(platform, "E")
		load = calc_load(platform)
		chk = platform_checksum(platform)
		if chk in checksums:
			break
		loads.append(load)
		checksums.append(chk)
	phase = checksums.index(chk)
	period = cycle - phase
	k = (1000000000-1 - phase) % period
	load = loads[phase + k]
	print("Part 2: load on North beam after 1000000000 cycles =", load)
	   

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