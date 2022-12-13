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

def compare_lists(a, b, lvl=0):

	if isTest:
		print("".join([" " for x in range(4*lvl)]), "Compare", a, "vs", b)
	
	for i in range(min(len(a), len(b))):
		if isinstance(a[i], list) and isinstance(b[i], list):
			v = compare_lists(a[i], b[i], lvl+1)
			if v != 0:
				return v
		elif isinstance(a[i], list) and isinstance(b[i], int):
			v = compare_lists(a[i], [b[i]], lvl+1)
			if v != 0:
				return v
		elif isinstance(a[i], int) and isinstance(b[i], list):
			v = compare_lists([a[i]], b[i], lvl+1)
			if v != 0:
				return v
		else:
			if a[i] < b[i]:
				return 1
			elif a[i] > b[i]:
				return -1
	if len(a) < len(b):
		return 1
	elif len(a) > len(b):
		return -1
	else: 
		return 0


def parse_list(text):
	text = text.replace("[", "[ ")
	text = text.replace("]", " ]")
	text = text.replace(",", " ")
	tokens = text.split(" ")

	stack = [[]]
	for t in tokens:
		if t == "[":
			n = []
			stack.append(n)
		elif t == "]":
			l = stack.pop()
			stack[-1].append(l)
		elif t.isalnum():
			stack[-1].append(int(t))

	return stack[-1][-1]


def main_1(inp):
	i = 0
	p = 0
	s = 0
	while i<len(inp):
		p += 1
		leftTxt = inp[i]
		left = parse_list(leftTxt)

		i += 1	
		rightTxt = inp[i]
		right = parse_list(rightTxt)

		if isTest:
			print(leftTxt)
			print(rightTxt)
			if compare_lists(left, right) != -1:
				s += p
				print("fine")
			else:
				print("REVERSED")
			print()

		i += 2
	print(s)


def main_2(inp):
	inp = [x for x in inp if x]
	inp.append("[[2]]")
	inp.append("[[6]]")

	# bubble sort the expanded list using the code from part 1
	swapped = True	
	while swapped:
		swapped = False
		for i in range(len(inp)-1):
			a = parse_list(inp[i])
			b = parse_list(inp[i+1])
			if compare_lists(a, b) == -1:
				tmp = inp[i]				
				inp[i] = inp[i+1]
				inp[i+1] = tmp
				swapped = True

	if isTest:
		for p in inp:
			print(p)

	v = 1
	i = 0
	for p in inp:
		i += 1
		if p == "[[2]]" or p == "[[6]]":
			v *= i
	print(v)


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