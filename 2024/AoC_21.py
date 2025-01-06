import os
import sys
from queue import PriorityQueue
from collections import defaultdict
from itertools import chain
import json

import AoC as aoc


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = False
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------


NUMPAD = [
	"789",
	"456",
	"123",
	" 0A"
]

KEYPAD = [
	" ^A",
	"<v>"
]

MOVES = {
	aoc.Vector(1, 0) : ">",
	aoc.Vector(-1, 0) : "<",
	aoc.Vector(0, 1) : "v",
	aoc.Vector(0, -1) : "^",
}

MAX_COST = 1000000


ADJ_4 = [aoc.Vector(1, 0), aoc.Vector(0, -1), aoc.Vector(0, 1), aoc.Vector(-1, 0)]


def gen_shortest_matrix(grid):
	matrix = {}

	bounds = [aoc.Vector(), aoc.Vector(len(grid[0]), len(grid))]

	for y in range(bounds[1].y):
		for x in range(bounds[1].x):
			if grid[y][x] == " ":
				continue
			start = aoc.Vector(x, y)
			startVal = grid[y][x]
			submatrix = {}
			for j in range(bounds[1].y):
				for i in range(bounds[1].x):
					if grid[j][i] == " ":
						continue
					end = aoc.Vector(i, j)
					endVal = grid[j][i]

					open = PriorityQueue()
					costs = defaultdict(lambda:MAX_COST)
					preds = defaultdict(lambda:None)

					costs[start] = 0
					open.put((0, start))
					
					path = []
					while not open.empty():
						loc = open.get()
						cost = loc[0]
						pos = loc[1]
						
						costs[pos] = cost

						if pos == end:
							while pos:
								path.append(pos)
								pos = preds[pos]
							path = path[::-1]
							moves = ""
							for i, p in enumerate(path[:-1]):
								d = path[i+1] - p
								moves += MOVES[d]
							break

						for ndir in ADJ_4:
							npos = pos + ndir
							ncost = cost + 1
							if npos.is_inside(*bounds) and grid[npos.y][npos.x] != " ":
								if ncost < costs[npos]:
									preds[npos] = pos
									tup = (ncost, npos)
									if not tup in open.queue:
										open.put(tup)
					submatrix[endVal] = moves
			matrix[startVal] = submatrix
	return matrix


def move_for_sequences(matrix, sequence):
		moves = ""
		sequence = "A" + sequence
		for i, v in enumerate(sequence[:-1]):
			moves += matrix[v][sequence[i+1]] + "A"
		return moves


def main_1(inp):
	
	matrixNumpad = gen_shortest_matrix(NUMPAD)
	print(json.dumps(matrixNumpad, indent=2))
	matrixKeypad = gen_shortest_matrix(KEYPAD)
	print(json.dumps(matrixKeypad, indent=2))

	print(move_for_sequences(matrixKeypad, "^A<<^^A>>AvvvA"))
	print(move_for_sequences(matrixKeypad, move_for_sequences(matrixKeypad, "^A<<^^A>>AvvvA")))

	print(move_for_sequences(matrixKeypad, "^A^^<<A>>AvvvA"))
	print(move_for_sequences(matrixKeypad, move_for_sequences(matrixKeypad, "^A^^<<A>>AvvvA")))

	complexity = 0
	for line in inp:
		numpadMoves = move_for_sequences(matrixNumpad, line)
		print("moves on Numpad to dial", line, ":", numpadMoves)

		keypadMoves = move_for_sequences(matrixKeypad, numpadMoves)
		print("moves on Keypad to dial", numpadMoves, ":", keypadMoves)

		keypadMoves2 = move_for_sequences(matrixKeypad, keypadMoves)
		print("moves on Keypad to dial", keypadMoves, ":", keypadMoves2)

		c = int(line[:-1]) * len(keypadMoves2)
		complexity += c
		print("complexity:", int(line[:-1]), "x", len(keypadMoves2), "=",c)

	print("total complexity:", complexity)

# example from website
# W: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# m: v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A>^AA<A>Av<A<A>>^AAAvA^<A>A
# W: <A>Av<<AA>^AA>AvAA^A<vAAA>^A
# m: <A>A<AAv<AA>>^AvAA^Av<AAA>^A
# W: ^A<<^^A>>AvvvA
# m: ^A^^<<A>>AvvvA

# my solution
# 379A

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