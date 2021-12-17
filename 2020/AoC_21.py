import os
import sys
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------


def main_1(inp):
	foods = []
	allergens = {}
	for line in inp:
		ingr, alle = line[:-1].split(" (contains ")
		f = [ingr.split(" "), alle.split(", ")]
		foods.append(f)
		for a in f[1]:
			if a not in allergens:
				allergens[a] = {}
			for i in f[0]:
				if i in allergens[a]:
					allergens[a][i] += 1
				else:
					allergens[a][i] = 1

	loop = True
	identified = {}
	while loop:
		loop = False
		for k, v in allergens.items():
			earlyOut = False
			for a, b in identified.items():
				if k in b:
					earlyOut = True
					break
			if earlyOut:
				continue

			maxC = 0
			maxI = ""
			for i, c in v.items():
				if i not in identified and c > maxC:
					maxC = c
					maxI = i
			count = 0
			for i, c in v.items():
				if i not in identified and c == maxC:
					count += 1 
			if count == 1:
				identified[maxI] = k
				loop = True

	ingredients = {}
	count = 0
	for f in foods:
		for i in f[0]:
			if i not in identified:
				count += 1 
				if i in ingredients:
					ingredients[i] += 1
				else: 
					ingredients[i] = 1
	
	print(json.dumps(foods, indent=4))
	print(json.dumps(allergens, indent=4))
	print(json.dumps(identified, indent=4))
	print(json.dumps(ingredients, indent=4))
	print(len(allergens))
	print(count)

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