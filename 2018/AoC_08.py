import os
import sys
import re
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def read_tree(stream, pos, parent, nodes):
	nb_children = stream[pos]
	children = []
	
	nb_meta = stream[pos+1]
	meta = []
	
	node = {"children": children, "meta": meta, "value": 0 }
	parent["children"].append(node)
	nodes.append(node)

	consumed = 2
	for i in xrange(0, nb_children):
		consumed += read_tree(stream, pos + consumed, node, nodes)
	
	for m in xrange(0, nb_meta):
		meta.append(stream[pos + consumed + m])
	stream = stream[nb_meta:]

	if len(children) > 0:
		for m in meta:
			if m-1 < len(children):
				node["value"] += children[m-1]["value"]
	else:
		node["value"] = sum(meta)

	return consumed + nb_meta
		


def main_1(inp):
	stream = [int(x) for x in inp[0].split(" ")]
	root = {"children": [], "meta": [] }
	nodes = []
	read_tree(stream, 0, root, nodes)
	s = 0
	for n in nodes:
		s += sum(n["meta"])
	print s


def main_2(inp, cost, nb):
	stream = [int(x) for x in inp[0].split(" ")]
	root = {"children": [], "meta": [], "value": 0 }
	nodes = []
	read_tree(stream, 0, root, nodes)
	print root["children"][0]["value"]


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
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = read_input(sys.argv[0].replace(".py", "_input.txt"))

	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		for t in xrange(0, len(tests)):
			if enablePart1:
				print "--- Test #" + str(t+1) + ".1 ------------------------------"
				main_1(tests[t])
			if enablePart2:
				print "--- Test #" + str(t+1) + ".2 ------------------------------"
				main_2(tests[t], 0, 2)
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		if enablePart1:
			print "--- Part 1 ------------------------------"
			main_1(inp)
		if enablePart2:
			print "--- Part 2 ------------------------------"
			main_2(inp, 60, 5)