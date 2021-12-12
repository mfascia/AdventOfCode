import os
import sys
import json
import copy


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
nbTests = 3
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------

def step(graph, paths, path, node):
	path.append(node)
	if node == "end":
		paths.append([x for x in path])
		return

	if node in graph:
		for n in graph[node]:
			if n.isupper() or n not in path:
				step(graph, paths, path, n)
				path.pop()
		

def main_1(inp):
	caves = {}
	for line in inp:
		a, b = line.split("-")
		if a not in caves:
			caves[a] = [b]
		else:
			if b not in caves[a]:
				caves[a].append(b)
		if b not in caves:
			caves[b] = [a]
		else:
			if a not in caves[b]:
				caves[b].append(a)
	
	paths = []
	path = []
	step(caves, paths, path, "start")
	print(len(paths))

def main_2(inp):
	caves = {}
	small = []
	for line in inp:
		a, b = line.split("-")

		if a.islower() and a not in small and a != "start" and a != "end":
			small.append(a)
		if b.islower() and b not in small and b != "start" and b != "end":
			small.append(b)

		if a not in caves:
			caves[a] = [b]
		else:
			if b not in caves[a]:
				caves[a].append(b)
		if b not in caves:
			caves[b] = [a]
		else:
			if a not in caves[b]:
				caves[b].append(a)
	
	allPaths = []
	for s in small:
		extended = copy.deepcopy(caves)
		extended[s+"__copy"] = [x for x in caves[s]]
		for l in caves[s]:
			extended[l].append(s+"__copy")
				
		paths = []
		path = []
		step(extended, paths, path, "start")
		for p in paths:
			pStr = "".join(p)
			allPaths.append(pStr)

	uniquePaths = {}
	for i in range(0, len(allPaths)):
		allPaths[i] = allPaths[i].replace("__copy", "")
		if allPaths[i] not in uniquePaths:
			uniquePaths[allPaths[i]] = True
	
	print(len(uniquePaths))


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
		for t in range(0, min(nbTests, len(tests))):
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