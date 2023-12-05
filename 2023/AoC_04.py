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

def parse(text):
	cards = []
	for line in text:
		card_num, values =  line.split(":")
		winners_text, numbers_text = values.split("|")
		winners_text = winners_text.replace("  ", " ").strip(" ")
		numbers_text = numbers_text.replace("  ", " ").strip(" ")
		winners = [int(x) for x in winners_text.split(" ")]
		numbers = [int(x) for x in numbers_text.split(" ")]
		cards.append([len(cards), 1, winners, numbers])
	return cards


def matches(card):
	count = 0
	for n in card[3]:
		if n in card[2]:
			count += 1
	return count


def main_1(inp):
	sum = 0
	cards = parse(inp)
	for c in cards:
		m = matches(c)
		if m > 0:
			value = 1 << (m-1)
		else:
			value = 0
		sum += value
	print("Part 1:", sum)


def main_2(inp):
	cards = parse(inp)
	for i in range(len(cards)):
		c = cards[i]
		m = matches(c)
		for k in range(i+1, min(len(cards), i+1+m)):
			cards[k][1] += c[1]
	count = 0
	for c in cards:
		count += c[1]

	print("Part 2:", count)


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