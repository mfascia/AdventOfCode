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
enablePart2 = True
#-----------------------------------------------------------------------------------------------

def step(code, state):
	inst = code[state["pc"]][:3]
	arg = int(code[state["pc"]][4:])

	if inst == "nop":
		state["pc"] += 1
	
	elif inst == "acc":
		state["acc"] += arg
		state["pc"] += 1

	elif inst == "jmp":
		state["pc"] += arg


def main_1(inp):
	state = {
		"acc":0,
	 	"pc": 0
		}
	pcs = []
	while state["pc"] < len(inp) and state["pc"] not in pcs:
		pcs.append(state["pc"])
		step(inp, state)
	
	print(json.dumps(state, indent=4))


def main_2(inp):
	for mutate in range(0, len(inp)):
		if inp[mutate] == "acc":
			continue

		code = [x for x in inp]
		if code[mutate][:3] == "nop":
			code[mutate] = "jmp" + code[mutate][3:]
			print("Mutating line", mutate, "from nop to jmp")
		else:
			code[mutate] = "nop" + code[mutate][3:]
			print("Mutating line", mutate, "from jmp to nop")

		state = {
			"acc":0,
			"pc": 0
			}
		pcs = []
		while state["pc"] < len(code) and state["pc"] not in pcs:
			pcs.append(state["pc"])
			step(code, state)

		if state["pc"] == len(code):
			print(json.dumps(state, indent=4))
			break



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