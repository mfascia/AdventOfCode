import sys


def read_input(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def hash_point(point):
    hash = 100000*point[0] + point[1]
    return hash


def process(code, visited):
    pos = [0, 0]
    hash = hash_point(pos)
    if visited.has_key(hash):
        visited[hash][1] += 1
    else:
        visited[hash] = [pos, 1]

    for c in code:
        new = [x for x in pos]
        if c == "^":
            new[1] += 1
        elif c == "v":
            new[1] -= 1
        elif c == ">":
            new[0] += 1
        elif c == "<":
            new[0] -= 1
        hash = hash_point(new)
        if visited.has_key(hash):
            visited[hash][1] += 1
        else:
            visited[hash] = [new, 1]
        pos = new


def main_1(text):
    visited = {}

    process(text[0], visited)
    
    print "Visited " + str(len(visited))


def main_2(text):
    visited = {}

    santa = text[0][0::2]
    robo = text[0][1::2]

    process(santa, visited)
    process(robo, visited)

    print "Visited " + str(len(visited))


if __name__ == "__main__":
	in_text = read_input("2015/03_in.txt")

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(in_text)

	print 

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(in_text)


"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?

For example:

    > delivers presents to 2 houses: one at the starting location, and one to the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.

Your puzzle answer was 2572.
--- Part Two ---

The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.

Your puzzle answer was 2631.
"""