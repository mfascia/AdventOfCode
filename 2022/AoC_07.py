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
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def print_dir(dir, level):
	spaces = "".join(["+--" for x in range(0, level)])
	print(spaces + "> " + dir["name"], "(", dir["size"], ")")
	
	for k,v in dir["content"].items():
		if v["type"] == "directory":
			print_dir(v, level+1)
		else:
			print( spaces + "+--+ " + v["name"], "(", v["size"], ")")

		
def calc_size(node):
	s = 0
	for k, v in node["content"].items():
		if v["type"] == "directory":
			calc_size(v)
		s += v["size"]
	node["size"] = s


def build_tree(inp):
	curr = {
		"parent": None,
		"name": "",
		"type": "directory",
		"size": 0,
		"content": {}
	}
	root = {
		"parent": curr,
		"name": "/",
		"type": "directory",
		"size": 0,
		"content": {}
	}
	curr["content"]["/"] = root

	for line in inp:
		if "$ cd" in line:
			if ".." in line:
				curr = curr["parent"]
			else:
				curr = curr["content"][line[5:]]
		elif "$ ls" in line:
			pass

		elif "dir" in line:
			node = {
				"parent": curr,
				"name": line[4:],
				"type": "directory",
				"size": 0,
				"content": {}
			}
			curr["content"][node["name"]] = node

		else:
			s, n = line.split(" ")
			curr["content"][n] = {
				"name": n,
				"type": "file",
				"size": int(s)
			}

	calc_size(root)
	return root


def find_small_folders(node, size, folders):
	if node["size"] <= size:
		folders.append(node)

	for k,v in node["content"].items():
		if v["type"] == "directory":
			find_small_folders(v, size, folders)


def find_big_folders(node, size, folders):
	if node["size"] >= size:
		folders.append(node)

	for k,v in node["content"].items():
		if v["type"] == "directory":
			find_big_folders(v, size, folders)


def main_1(inp):
	root = build_tree(inp)
	#print_dir(root, 0)
	small = []
	find_small_folders(root, 100000, small)
	total = sum(map(lambda x: x["size"], small))
	print(total)


def main_2(inp):
	root = build_tree(inp)
	free = 70000000 - root["size"]
	toFree = max(30000000 - free, 0)
	print("need to free", toFree)
	big = []
	find_big_folders(root, toFree, big)
	toDelete = min(big, key= lambda x: x["size"])
	print(toDelete["size"], toDelete["name"])


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