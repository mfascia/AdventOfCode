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
#-----------------------------------------------------------------------------------------------

def differentiate(signal):
	deriv = []
	for i in range(len(signal)-1):
		deriv.append(signal[i+1] - signal[i])
	return deriv

def is_zero_signal(signal):
	return sum(map(lambda x: x == 0, signal)) == len(signal)


def parse(text):
	histories = []
	for line in text:
		hist = [int(x) for x in line.split(" ")]
		histories.append(hist)
	return histories


def main(inp):
	histories = parse(inp)

	total_1 = 0
	total_2 = 0
	for h in histories:
		signal = h

		derivatives = []
		while not is_zero_signal(signal):
			derivatives.append(signal)
			signal = differentiate(signal)
		
		diff = 0
		for d in derivatives[::-1]:
			diff = d[-1] + diff
			d.append(diff)

		diff = 0
		for d in derivatives[::-1]:
			diff = d[0] - diff
			d.insert(0, diff)

		total_1 += derivatives[0][-1]
		total_2 += derivatives[0][0]

	print("Part 1:", total_1)
	print("Part 2:", total_2)


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
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		main(inp)