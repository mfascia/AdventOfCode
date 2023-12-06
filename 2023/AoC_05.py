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


def parse_map(text, i):
	mapping = []
	while i<len(text) and text[i] != "":
		mapping.append([int(x) for x in text[i].split(" ")])
		i += 1
	mapping.sort(key=lambda x: x[1])
	return i, mapping


def transform_value(mapping, value):
	for m in mapping:
		delta = value - m[1]
		if delta >=0 and delta < m[2]:
			return m[0] + delta
	return value


def transform_interval(mapping, interval):
	ins = [interval]
	outs = []
	while ins:
		i = ins.pop(0)
		transformed = False
		a = i[0]
		b = i[0] + i[1]
		for m in mapping:
			c = m[1]
			d = m[1] + m[2]
			if a < c:
				if b > d:
					#---a--------b--------
					#-----c---d-----------
					ins.append([a, c-a])	
					ins.append([d, b-d])
					outs.append([m[0], m[2]])
					transformed = True
					break
				elif b > c and b <= d:
					#---a-----b-------------
					#-----c-----d-----------
					ins.append([a, c-a])	
					outs.append([m[0], b-c])
					transformed = True
					break
			elif a < d:
				if b > d:
					#-----a--------b-------
					#---c------d-----------
					ins.append([d, b-d])	
					outs.append([m[0] + a-c, d-a])
					transformed = True
					break
				elif b <= d:
					#-----a-----b----------
					#---c---------d--------
					outs.append([m[0] + a-c, b-a])
					transformed = True
					break
		if not transformed:
			outs.append([a, b-a])
	return outs

def parse(inp):
	seeds = [int(x) for x in inp[0][7:].split(" ")]
	maps = []
	i = 1
	for j in range(7):
		i, m = parse_map(inp, i+2)
		maps.append(m)

	return seeds, maps


def main_1(inp):
	seeds, maps = parse(inp)

	locations = []
	for s in seeds:
		d = s
		for m in maps:
			d = transform_value(m, d)
		locations.append(d)
		print(s, "->", d)

	print("Part 1:", min(locations))


def main_2(inp):
	seeds, maps = parse(inp)

	ins = []
	for s in range(0, len(seeds), 2):
		ins.append([seeds[s], seeds[s+1]])

	for m in maps:
		outs = []
		for i in ins: 
			o = transform_interval(m, i)
			outs += o
		ins, outs = outs, ins

	ins.sort(key=lambda x: x[0])
	print("Part 2:", ins[0][0])
		

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