import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False
part = 0

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------

CARDS = "23456789TJQKA"
CARDPOS = {
	"2": 0,
	"3": 1,
	"4": 2,
	"5": 3,
	"6": 4,
	"7": 5,
	"8": 6,
	"9": 7,
	"T": 8,
	"J": 9,
	"Q": 10,
	"K": 11,
	"A": 12,
}


def value(card):
	if card == "J" and part == 2:
		return 0
	else:
		return CARDPOS[card] + 1


def parse_hand(text):
	cards, bid = text.split(" ")
	return cards, int(bid)


def score_hand(cards):
	histogram = [0 for x in range(len(CARDS))]
	for c in cards:
		histogram[CARDPOS[c]] += 1

	score = 0
	if 5 in histogram:
		score = 6
	elif 4 in histogram:
		score = 5
	elif 3 in histogram:
		if 2 in histogram:
			score = 4
		else:
			score = 3
	elif sum([1 if h == 2 else 0 for h in histogram ]) == 2:
		score = 2
	elif 2 in histogram:
		score = 1

	return score
	

def replace_jokers(cards):
	if "J" in cards:
		orig = cards
		cards = cards.replace("J", "")
		histogram = [0 for x in range(len(CARDS))]
		for c in cards:
			histogram[CARDPOS[c]] += 1

		# Replace Jokers with the card with highest occurence.
		# In case of 2 pairs, pick the card with highest value.
		# In case of 5 jokers, replcae with 5 As.
		if sum([1 if h == 2 else 0 for h in histogram ]) == 2:
			v1 = histogram.index(2)
			v2 = len(histogram) - histogram[::-1].index(2) - 1
			if v1 > v2:
				cards = orig.replace("J", CARDS[v1])
			else:
				cards = orig.replace("J", CARDS[v2])
		elif cards == "":
			cards = "AAAAA"
		else:
			cards = orig.replace("J", CARDS[histogram.index(max(histogram))])
	
	return cards


def rank(hand):
	return score_hand(hand[0]) * 10000000000 + value(hand[0][0]) * 100000000 + value(hand[0][1]) * 1000000 + value(hand[0][2]) * 10000 + value(hand[0][3]) * 100 + value(hand[0][4])


def rank_with_jokers(hand):
	return score_hand(hand[1]) * 10000000000 + value(hand[0][0]) * 100000000 + value(hand[0][1]) * 1000000 + value(hand[0][2]) * 10000 + value(hand[0][3]) * 100 + value(hand[0][4])


def main_1(inp):
	hands = []
	for line in inp:
		cards, bid = parse_hand(line)
		hands.append([cards, bid])
	
	hands.sort(key=rank)	
	
	winnings = 0
	for i in range(len(hands)):
		winnings += (i+1) * hands[i][1]

	print(winnings)


def main_2(inp):
	hands = []
	for line in inp:
		cards, bid = parse_hand(line)
		best = replace_jokers(cards)
		hands.append([cards, best, bid])
	
	hands.sort(key=rank_with_jokers)	
	
	winnings = 0
	for i in range(len(hands)):
		winnings += (i+1) * hands[i][2]

	print(winnings)


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
			part = 1
			if enablePart1:
				print ("--- Test #" + str(t+1) + ".1 ------------------------------")
				main_1(tests[t])
			part = 2
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
		part = 1
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		part = 2
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)