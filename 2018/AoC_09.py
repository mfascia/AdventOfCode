import os
import sys
import re
from collections import deque


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = [
	"9 players; last marble is worth 25 points",
	"10 players; last marble is worth 1618 points: high score is 8317",
	"13 players; last marble is worth 7999 points: high score is 146373",
	"17 players; last marble is worth 1104 points: high score is 2764",
	"21 players; last marble is worth 6111 points: high score is 54718",
	"30 players; last marble is worth 5807 points: high score is 37305"
]
inp1 = "405 players; last marble is worth 70953 points"
inp2 = "405 players; last marble is worth 7095300 points"

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def print_game(buffer, pos, player):
	line =  "[" + str(player+1) + "] "
	for i in xrange(0, len(buffer)):
		if i == pos:
			line += "(" + format(buffer[i], "5d") + ")"
		else:
			line += " " + format(buffer[i], "5d") + " "
	print line


def main(inp):
	match = re.match("([0-9]*) players; last marble is worth ([0-9]*) points", inp)
	nbPlayers = int(match.group(1))
	lastMarbleValue = int(match.group(2))
	print nbPlayers, lastMarbleValue

	players = [0 for x in xrange(0, nbPlayers)]
	p = 0
	buffer = deque([0])
	pos = 0
	val = 1
	#print_game(buffer, pos, p)
	while val <= lastMarbleValue:
		if val % 23 == 0:
			buffer.rotate(7)
			players[p] += val + buffer.pop()
			buffer.rotate(-1)
		else:
			buffer.rotate(-1)
			buffer.append(val)
		#print_game(buffer, pos, p)
		val += 1
		p = (p+1) % nbPlayers

	print "player", players.index(max(players))+1, "has max score of", max(players)


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
					tests.append(read_input(testfile))
				else:
					break

	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		for t in xrange(0, len(tests)):
			if enablePart1:
				print "--- Test #" + str(t+1) + " ------------------------------"
				main(tests[t])
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main(inp1)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main(inp2)