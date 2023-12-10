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
#-----------------------------------------------------------------------------------------------


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# Reminder: Positive Y goes down 

VALID = {
	"S": [(1, 0), (-1, 0), (0, 1), (0, -1)],
	"|": [(0, 1), (0, -1)],
	"-": [(1, 0), (-1, 0)],
	"L": [(1, 0), (0, -1)],
	"J": [(-1, 0), (0, -1)],
	"7": [(-1, 0), (0, 1)],
	"F": [(1, 0), (0, 1)],
	".": []
 }

NEIGHBOURS = [
	[-1, 0],
	[+1, 0],
	[0, -1],
	[0, +1],
]


def parse_pipes(text):
	w = len(text[0]) + 2
	h = len(text) + 2
	pipes = ["." + y + "."for y in text]
	pipes.insert(0, "".join(["." for x in range(w)]))
	pipes.append("".join(["." for x in range(w)]))
	
	sx = -1
	sy = -1
	for y in range(h):
		for x in range(w):
			if pipes[y][x] == "S":
				sx = x
				sy = y
				break
	return w, h, pipes, sx, sy


def print_pipes(pipes):
	for y in range(len(pipes)):
		print("".join(pipes[y]))


def print_distancefield(pipes, caves, df, furthest):
	for y in range(len(df)):
		line = ""
		for x in range(len(df[0])):
			d = df[y][x]
			if d == -1:
				if caves[y][x] == 0:
					line += "I"
				else:
					line += " "
			elif d == furthest:
				line += "@"
			elif pipes[y][x] in ".S-|JL7F":
				line += ".S═║╝╚╗╔"[".S-|JL7F".find(pipes[y][x])]
		print(line)


def floodfill(src, dst, w, h, x, y, valid, c):
	queue = [(x, y)]
	count = 0
	while len(queue) > 0:
		px, py = queue.pop()
		if src[py][px] in valid and dst[py][px] != c:
			dst[py][px] = c
			count += 1
			neighbours = [tuple(n) for n in map(lambda k: (px+k[0], py+k[1]), NEIGHBOURS) if n[0]>=0 and n[0]<w and n[1]>=0 and n[1]<h]
			for n in neighbours:
				if dst[n[1]][n[0]] != c:
					queue.append(n)
	return count


def explore(pipes, w, h, sx, sy):
	df = [[-1 for x in pipes[0]] for y in pipes]
	df[sy][sx] = 0
	prev = (-1, -1)
	curr = (sx, sy)
	next = (-1, -1)
	looped = False
	while not looped > 0:
		for n in VALID[pipes[curr[1]][curr[0]]]:
			next = (curr[0] + n[0], curr[1] + n[1])
			if next[0] < 0 or next[0] >= w or next[1] < 0 or next[1] >= h:
				# no going out of bounds
				continue
			if (curr[0]-next[0], curr[1]-next[1]) not in VALID[pipes[next[1]][next[0]]]:
				# next needs to be actually connected to curr (solves the S case)
				continue
			elif pipes[next[1]][next[0]] == ".":
				# no exploring outside of pipes network
				continue
			elif next == prev:
				# no going backwards
				continue
			elif next[1] == sy and next[0] == sx:
				# reached the start, loop is complete
				looped = True
				break
			else:
				df[next[1]][next[0]] = df[curr[1]][curr[0]] + 1
				prev = curr
				curr = next
				break

	furthest = max(max(y) for y in df)
	print("Part 1: furthest =", (furthest + 1)//2)

	flooded = [[0 for x in range(w)] for y in range(h)]
	countDots = floodfill(pipes, flooded, w, h, 0, 0, ".", 1)
	countPipes = floodfill(pipes, flooded, w, h, sx, sy, "S|-JL7F", 2)

	print("Part 2: caves area =", (w)*(h) - countDots - countPipes) 
	print()

	print_distancefield(pipes, flooded, df, furthest)

	return df

def main(inp):
	width, height, pipes, sx, sy = parse_pipes(inp)
	print_pipes(pipes)

	if sx != -1 and sy != -1:
		df = explore(pipes, width, height, sx, sy)


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
			print ("--- Test #" + str(t+1) + "---------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		print ("--- Part 1 ------------------------------")
		main(inp)