'''
--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get - the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
R5, L5, R5, R3 leaves you 12 blocks away.
How many blocks away is Easter Bunny HQ?

Your puzzle answer was 231.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
'''

raw_input = "R5, R4, R2, L3, R1, R1, L4, L5, R3, L1, L1, R4, L2, R1, R4, R4, L2, L2, R4, L4, R1, R3, L3, L1, L2, R1, R5, L5, L1, L1, R3, R5, L1, R4, L5, R5, R1, L185, R4, L1, R51, R3, L2, R78, R1, L4, R188, R1, L5, R5, R2, R3, L5, R3, R4, L1, R2, R2, L4, L4, L5, R5, R4, L4, R2, L5, R2, L1, L4, R4, L4, R2, L3, L4, R2, L3, R3, R2, L2, L3, R4, R3, R1, L4, L2, L5, R4, R4, L1, R1, L5, L1, R3, R1, L2, R1, R1, R3, L4, L1, L3, R2, R4, R2, L2, R1, L5, R3, L3, R3, L1, R4, L3, L3, R4, L2, L1, L3, R2, R3, L2, L1, R4, L3, L5, L2, L4, R1, L4, L4, R3, R5, L4, L1, L1, R4, L2, R5, R1, R1, R2, R1, R5, L1, L3, L5, R2"


increments = [ 
	[0, 1],			# direction = 0 --> North
	[-1, 0], 		# direction = 1 --> West
	[0, -1], 		# direction = 2 --> South
	[1, 0] 			# direction = 3 --> East
]


def main_1():
	input = raw_input.split(", ")

	direction = 0
	x = 0
	y = 0

	for step in input:
		if step[0] == "R":
			direction = 3 if direction == 0 else direction - 1
		elif step[0] == "L":
			direction = 0 if direction == 3 else direction + 1
		step = step[1:]

		x += increments[direction][0] * int(step)
		y += increments[direction][1] * int(step)

	print abs(x) + abs(y)


def main_2():
	input = raw_input.split(", ")

	direction = 0
	x = 0
	y = 0

	visited = []

	for step in input:
		if step[0] == "R":
			direction = 3 if direction == 0 else direction - 1
		elif step[0] == "L":
			direction = 0 if direction == 3 else direction + 1
		step = step[1:]

		dist = int(step)

		for s in xrange(0, dist):
			x += increments[direction][0]
			y += increments[direction][1]
			loc = [x, y]
			if loc not in visited:
				visited.append(loc)
			else:
				print abs(x) + abs(y)
				return


if __name__ == "__main__":
	main_1()	
	main_2()