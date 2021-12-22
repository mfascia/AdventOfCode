import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = [ [4, 8] ]
inp = [3, 4]
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def main_1(inp):

	dice = 1
	scores = [0, 0]
	positions = [x for x in inp]
	player = 0
	rolls = 0
	while max(scores) < 1000:
		for r in range(3):
			positions[player] += dice
			while positions[player] > 10:
				positions[player] -= 10
			dice += 1
			if dice == 101:
				dice = 1
			rolls += 1
		scores[player] += positions[player]
		player = (player+1) % 2

	print(rolls*min(scores))


DICE_TOTAL_FREQS = {
	3: 1,
	4: 3,
	5: 6,
	6: 7,
	7: 6,
	8: 3,
	9: 1
}

def main_2(inp):
	# precompute the board logic into a lookup table
	outcomes = {}
	for i in range(1, 11):
		outcomes[i] = {}
		for j in range(3, 10):
			outcomes[i][j] = i+j if i+j <= 10 else i+j-10

	states = {}
	# Games: p1 score, p1 position, p2 score, p2 position
	states[(0, inp[0], 0, inp[1])] = 1
	# Number of wins for p1, p2
	wins = [0, 0]
	while len(states):
		newStates = {}
		for state, count in states.items():
			for dice1 in range(3, 10):
				for dice2 in range(3, 10):	
					# calculate new player positions on the board
					newPos1 = outcomes[state[1]][dice1]
					newPos2 = outcomes[state[3]][dice2]
					# accumulate player scores
					score1 = state[0] + newPos1
					score2 = state[2] + newPos2
					# check if p1 has one and if not, if p2 has won
					if score1 >= 21:
						wins[0] += count * DICE_TOTAL_FREQS[dice1]
					elif score2 >= 21:
						wins[1] += count * DICE_TOTAL_FREQS[dice1] * DICE_TOTAL_FREQS[dice2]

					else:
						newState = (score1, newPos1, score2, newPos2)
						if newState in newStates:
							newStates[newState] += count * DICE_TOTAL_FREQS[dice1] * DICE_TOTAL_FREQS[dice2]
						else:
							newStates[newState] = count * DICE_TOTAL_FREQS[dice1] * DICE_TOTAL_FREQS[dice2]
		states = newStates

	# Player 1 wins needs to be divided by 7. The reason is because the cumulated count
	# includes all the states where the winning player 1 dice rolls are followed 
	# by the 7 possible dice rolls for player 2 
	wins[0] = int(wins[0]/7)
	
	print(max(wins))


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