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
enablePart2 = True
#-----------------------------------------------------------------------------------------------


TOWER_WIDTH = 7
HORIZONTAL_CLEARANCE = 2
VERTICAL_CLEARANCE = 3
TOWER_ROWS_FOR_PATTERN_MATCHING = 16 # This was set through manual iteration. any larger number yield the same result as 16


ROCKS = [
	# extents	rock positions
	[ (4, 1), 	[(0, 0), (1, 0), (2, 0), (3, 0)]			],			# -
	[ (3, 3), 	[(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)] 	],			# +
	[ (3, 3), 	[(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)] 	],			# _|
	[ (1, 4), 	[(0, 0), (0, 1), (0, 2), (0, 3)] 			],			# |
	[ (2, 2), 	[(0, 0), (0, 1), (1, 0), (1, 1)] 			]			# o
]


class Rock:
	def __init__(self, model, pos):
		self.model = model
		self.pos = pos

	def overlap(self, tower):
		for y in range(ROCKS[self.model][0][1]):
			for x in range(ROCKS[self.model][0][0]):
				p = (x, y)
				if p in ROCKS[self.model][1] and tower[self.pos[1]-y][self.pos[0]+x] == 1:
					return True

	def try_move(self, tower, p):
		if p[0] < 0:
			return False
		if p[0] + (ROCKS[self.model][0][0]-1) >= TOWER_WIDTH:
			return False
		if p[1] - (ROCKS[self.model][0][1]-1) < 0:
			return False
		op = self.pos
		self.pos = p
		if self.overlap(tower):
			self.pos = op
			return False
		else:
			return True

	def add_to_tower(self, tower):
		for y in range(ROCKS[self.model][0][1]):
			for x in range(ROCKS[self.model][0][0]):
				p = (x, y)
				if p in ROCKS[self.model][1]:
					tower[self.pos[1]-y][self.pos[0]+x] = 1


def print_tower(tower, rock=None):
	print()
	for y in range(len(tower)-1, -1, -1):
		line = "|"
		for x in range(TOWER_WIDTH):
			if rock and (x-rock.pos[0], rock.pos[1]-y) in ROCKS[rock.model][1]:
				line += "@"
			elif tower[y][x] == 1:
				line += "#"
			else:
				line += "."
		line += "|"
		if y % 5 == 0:
			line += " " + str(y)
		print(line)
	print("+" + "".join	(["-" for x in range(TOWER_WIDTH)]) + "+")


def run_game(wind, nbRocks):
	rockIndex = 0
	rocks = []
	tower = []
	top = -1
	w = 0
	for r in range(nbRocks):
		# add lines to the tower if needed
		need = ROCKS[rockIndex][0][1] + VERTICAL_CLEARANCE
		has = len(tower) - top - 1
		for add in range(need-has):
			tower.append([0 for x in range(TOWER_WIDTH)])

		# spawn new rock
		rock = Rock(rockIndex, (HORIZONTAL_CLEARANCE, top + need))
		rockIndex = (rockIndex+1) % len(ROCKS)

		# if isTest: print_tower(tower, rock)

		# make rock fall
		while True:
			# apply wind
			if wind[w] == ">":
				rock.try_move(tower, (rock.pos[0]+1, rock.pos[1]))
			else:
				rock.try_move(tower, (rock.pos[0]-1, rock.pos[1]))
			w = (w + 1) % len(wind)

			# move down
			if not rock.try_move(tower, (rock.pos[0], rock.pos[1]-1)):
				break

		# add the rock to the tower when it stopped
		rock.add_to_tower(tower)
		top = max(top, rock.pos[1])

	return top


def main_1(inp):
	print(run_game(inp[0], 2022) + 1)




def run_long_game(wind, nbRocks):
	rockIndex = 0
	rocks = []
	tower = []
	top = -1
	w = 0
	hist = {}

	matched = False
	
	r = 0
	while r < nbRocks:
		# add lines to the tower if needed
		need = ROCKS[rockIndex][0][1] + VERTICAL_CLEARANCE
		has = len(tower) - top - 1
		for add in range(need-has):
			tower.append([0 for x in range(TOWER_WIDTH)])

		# spawn new rock
		rock = Rock(rockIndex, (HORIZONTAL_CLEARANCE, top + need))
		rockIndex = (rockIndex+1) % len(ROCKS)

		# if isTest: print_tower(tower, rock)

		# make rock fall
		while True:
			# apply wind
			if wind[w] == ">":
				rock.try_move(tower, (rock.pos[0]+1, rock.pos[1]))
			else:
				rock.try_move(tower, (rock.pos[0]-1, rock.pos[1]))
			w = (w + 1) % len(wind)

			# move down
			if not rock.try_move(tower, (rock.pos[0], rock.pos[1]-1)):
				break

		# add the rock to the tower when it stopped
		rock.add_to_tower(tower)
		top = max(top, rock.pos[1])
		
		# store the state of the rock that has settled and try to match with previous rocks
		# state is a tuple comprised of: wind, rock type, string representing the top of the tower 
		if top > TOWER_ROWS_FOR_PATTERN_MATCHING and not matched:
			repr = ""
			for row in tower[-1:-TOWER_ROWS_FOR_PATTERN_MATCHING:-1]:
				repr += "".join(["." if x == 0 else "#" for x in row])
			state = (repr, rockIndex, w)
			if state in hist:
				# we have a match!
				matched = True
				h0 = hist[state][1] 					# h0 = how tall the tower before the start of the repeating pattern 
				hp = top - h0							# hp = the height of the bit that repeats
				h1 = top								# h1 = the height at the point where the first instance of the pattern ends
				period = r - hist[state][0]				# number of block that form the pattern
				repeats = int((nbRocks - r) / period)	# how many times the pattern still repeats after the first occurence
				nbRocks = (nbRocks - r) % period		# nb of rock of the incomplete pattern at the top
				r = -1
			else:
				hist[state] = (r, top)

		r += 1

	return h1 + hp * repeats + (top-h1)


def main_2(inp):
	print(run_long_game(inp[0], 1000000000000))			


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