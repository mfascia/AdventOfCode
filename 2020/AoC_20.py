import os
import sys
import json



# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------

def nbMatchedEdges(tile):
	score = 0
	for e in tile["matches"]:
		if len(e) > 0:
			score += 1
		if len(e)>1:
			print(json.dumps(values, indent=4))
	return score


def main_1(inp):
	tiles = {}
	for i in range(0, len(inp), 12):
		line = inp[i]
		tile = {}
		_, id = line.split(" ")
		tile["id"] = int(id[:-1])
		tile["raw_data"] = "".join(inp[i+1:i+11])
		tile["bin_data"] = tile["raw_data"].replace(".", "0").replace("#", "1")
		tile["edges"] = [] # N,rN, S,rS, E,rE, W,rW
		
		binStr = tile["bin_data"][0:10]
		tile["edges"].append(int(binStr,2))
		tile["edges"].append(int(binStr[::-1],2))

		binStr = tile["bin_data"][90:]
		tile["edges"].append(int(binStr,2))
		tile["edges"].append(int(binStr[::-1],2))

		binStr = "".join([tile["bin_data"][x+9] for x in range(0, 100, 10)])
		tile["edges"].append(int(binStr,2))
		tile["edges"].append(int(binStr[::-1],2))

		binStr = "".join([tile["bin_data"][x] for x in range(0, 100, 10)])	
		tile["edges"].append(int(binStr,2))
		tile["edges"].append(int(binStr[::-1],2))
		tile["matches"] = [[] for x in range(0,8)]

		tiles[tile["id"]] = tile

	values = [v for v in tiles.values()]
	for i in range(0, len(values)):
		for j in range(i+1, len(values)):
			for a in range(0, 8):
				for b in range(0, 8):
					if values[i]["edges"][a] == values[j]["edges"][b]:
						values[i]["matches"][a].append(values[j]["id"])
						values[j]["matches"][b].append(values[i]["id"])
						
	for i in range(0, len(values)):
		values[i]["Nb_mathce_edges"] = 0

	values = sorted(values, key=lambda x: nbMatchedEdges(x))
	#print(values[0:4])
	print(values[0]["id"] * values[1]["id"] * values[2]["id"] * values[3]["id"])
	#print(json.dumps(values, indent=4))



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
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)